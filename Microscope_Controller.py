import math
from tkinter import *
from tkinter import ttk

from UI_Microscope import Ui_MicroscopeMainWindow
from OlympusBX3MCBFM import OlympusBX3MCBFM
from PriorES10ZE import PriorES10ZE


class main_window(Ui_MicroscopeMainWindow):
    def __init__(self):
        super().__init__()

        self.root.objective_frame.objective_kinds = ['x5', 'x10', 'x20', 'x50', 'x100']

        self.root.objective_frame.objective_buttons = [
                ttk.Button(
                    self.root.objective_frame, text = i, command = self.objective_button_cmd(i)
                ) for i in self.root.objective_frame.objective_kinds
            ]
        for button in self.root.objective_frame.objective_buttons:
            button.pack(fill = BOTH, expand = 1, padx = 5, pady = 5)

        ttk.Scale(self.root.focus_frame.focus_speed_frame, 
                from_ = 0.0, to = 3.0, variable = self.root.focus_frame.focus_speed_exp, 
                command = self.scale_command
            ).pack(side = LEFT, fill = X, expand = 1, padx = 5)

        self.root.focus_frame.focus_speed.trace('w', self.focus_speed_cmd)
        self.root.focus_frame.focus_speed_field.trace(
                'w', self.focus_speed_field_cmd 
            )

        for button in self.root.focus_frame.focus_buttons:
            button.bind(
                    '<Button-1>', self.focus_button_pressed(button['text'])
                )
            button.bind('<ButtonRelease-1>', self.focus_button_released)

        self.root.focus_frame.focus_speed_frame.val_cmd \
            = self.root.focus_frame.focus_speed_frame.register(
                lambda P: False if not P.isdecimal() or int(P) > 1000 \
                    else True
            )

    def focus_speed_cmd(self, *args):
        self.root.focus_frame.focus_speed_exp.set(math.log10(
                self.root.focus_frame.focus_speed.get()
            ))
        self.root.focus_frame.focus_speed_frame.focus_speed_display['text'] \
            = self.root.focus_frame.focus_speed.get()

    def focus_speed_field_cmd(self, *args):
        if self.root.focus_frame.focus_speed_field.get():
            self.root.focus_frame.focus_speed.set(
                    self.root.focus_frame.focus_speed_field.get()
                )

    def focus_button_pressed(self, kind):
        def inner(*e):
            print(
                    f'C {self.root.focus_frame.focus_speed.get()}', 
                    f'''{kind}'''
                )
            with PriorES10ZE({'port': 'COM9'}) as p:
                p.send_command(
                        f'C {self.root.focus_frame.focus_speed.get()}'
                    )
                p.send_command(
                    f'''{kind}'''
                )
            self.root.focus_frame.job = self.root.after(
                    200, self.focus_button_pressed(kind)
                )
        return inner

    def focus_button_released(self, e):
        self.root.after_cancel(self.root.focus_frame.job)

    def scale_command(self, e):
        self.root.focus_frame.focus_speed.set(
                10**self.root.focus_frame.focus_speed_exp.get()
            )
        self.root.focus_frame.focus_speed_field.set('')

    def objective_button_cmd(self, kind):
        def inner():
            with OlympusBX3MCBFM({'port': 'COM7'}) as b:
                current_index, target_index = b.change_objective(kind)
                with PriorES10ZE() as p:
                    p.send_command('C 1')
                    p.send_command(
                        f'''U { p.position_list[ target_index ] - 
                            p.position_list[ current_index ] 
                        }'''
                    )
        return inner

def main():
    Microscope_main = main_window()
    Microscope_main.root.mainloop()

if __name__ == '__main__':
    main()