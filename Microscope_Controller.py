import math
from tkinter import *
from tkinter import ttk

from UI_JogandSwitch import UI_JogandSwitch
from OlympusBX3MCBFM import OlympusBX3MCBFM
from PriorES10ZE import PriorES10ZE


class main_window(UI_JogandSwitch):
    def __init__(self, master = None):
        goback_label = ['U', 'D']
        switch_number = 5
        super().__init__(master, goback_label, switch_number)

        style = ttk.Style(master)
        style.configure('white.TButton', background='white')
        style.configure('green.TButton', background='green')

        self.label['text'] = 'microscope'
        self.left_frame.speed_frame['text'] = 'focus speed'
        self.left_frame.label['text'] = 'focus'
        self.right_frame.label['text'] = 'objective'

        objective_kinds = ['x5', 'x10', 'x20', 'x50', 'x100']
        for button, kind in zip( self.right_frame.switch_buttons, objective_kinds):
            button['text'] = kind
            button['command'] = self.objective_button_cmd(kind)
        self.update_objective_button()

        self.left_frame.focus_speed_exp = DoubleVar(value= 0.0)
        self.left_frame.focus_speed = IntVar(value= 1)
        speed_scale_options = {
                'from_' : 0.0, 'to' : 3.0, 
                'variable' : self.left_frame.focus_speed_exp, 
                'command' : self.scale_command
            }
        for k in speed_scale_options.keys():
            self.left_frame.speed_frame.speed_scale[k] = speed_scale_options[k]

        self.left_frame.focus_speed.trace('w', self.focus_speed_cmd)

        for button in self.left_frame.goback_buttons:
            button.bind(
                    '<Button-1>', self.focus_button_pressed(button['text'])
                )
            button.bind('<ButtonRelease-1>', self.focus_button_released)

    def focus_speed_cmd(self, *args):
        self.left_frame.focus_speed_exp.set(math.log10(
                self.left_frame.focus_speed.get()
            ))
        self.left_frame.speed_frame.speed_display['text'] \
            = self.left_frame.focus_speed.get()

    def focus_button_pressed(self, kind):
        def inner(*e):
            with PriorES10ZE({'port': 'COM9'}) as p:
                p.send_command(
                        f'C {self.left_frame.focus_speed.get()}'
                    )
                p.send_command(
                    f'''{kind}'''
                )
            self.left_frame.job = self.after(
                    200, self.focus_button_pressed(kind)
                )
        return inner

    def focus_button_released(self, e):
        self.after_cancel(self.left_frame.job)

    def scale_command(self, e):
        self.left_frame.focus_speed.set(
                10**self.left_frame.focus_speed_exp.get()
            )

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
            self.update_objective_button()
        return inner

    def update_objective_button(self):
        with OlympusBX3MCBFM({'port': 'COM7'}) as b:
            self.current_objective = b.current_objective()
        for i, button in enumerate(self.right_frame.switch_buttons):
            button.configure(style = ('green' if i == self.current_objective - 1 else 'white') + '.TButton')

def main():
    master = Tk()
    master.bind('<Control-Key-c>', lambda e: master.quit())
    main_window(master).mainloop()

if __name__ == '__main__':
    main()