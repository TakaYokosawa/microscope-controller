import math
from tkinter import *
from tkinter import ttk

from UI_JogandSwitch import UI_JogandSwitch
from OptoSigmaSRC101 import OptoSigmaSRC101
from KEISEEDS_RBIO2U import KEISEEDS_RBIO2U


class main_window(UI_JogandSwitch):
    def __init__(self, master = None):
        goback_label = ['+', '-']
        switch_number = 9
        super().__init__(master, goback_label, switch_number)

        style = ttk.Style(master)
        style.configure('white.TButton', background='white')
        style.configure('green.TButton', background='green')

        self.label['text'] = 'stage'
        self.left_frame.speed_frame['text'] = 'move speed'
        self.left_frame.label['text'] = 'stage move'
        self.right_frame.label['text'] = 'axis change'

        ttk.Label(
                self.right_label_frame, text='stack', font=('Helvetica', '15', 'bold')#, justify = CENTER
            ).pack(side = LEFT, expand = True)
        ttk.Label(
                self.right_label_frame, text='sample', font=('Helvetica', '15', 'bold')
            ).pack(side = LEFT, expand = True)

        axis_kinds = ['x', 'y', 'z', 'Rx', 'Ry', 'x', 'y', 'z', 'R']
        for i, (button, kind) in enumerate(zip(self.right_frame.switch_buttons, axis_kinds)):
            button['text'] = kind
            button['command'] = self.axis_button_cmd(i)
        self.update_axis_button()

        self.is_continuous_move = BooleanVar(value= False)
        ttk.Checkbutton(
                self.move_option_frame, text = 'continuous', 
                variable = self.is_continuous_move
            ).pack(side = LEFT)
        self.stop_button = ttk.Button(
                self.move_option_frame, text = 'stop', 
                command = self.stop_stage_move, width = 6, state = 'disabled'
            )
        self.stop_button.pack()

        self.left_frame.move_speed = IntVar(value= 1)
        self.is_fine_move = BooleanVar(value= False)
        speed_scale_options = {
                'from_' : 1, 'to' : 48, 
                'variable' : self.left_frame.move_speed, 
            }
        for k in speed_scale_options.keys():
            self.left_frame.speed_frame.speed_scale[k] = speed_scale_options[k]

        ttk.Checkbutton(
                self.left_frame.speed_frame, text = 'fine', 
                variable = self.is_fine_move
            ).pack()
                
        self.left_frame.move_speed.trace('w', self.move_speed_cmd)

        for button in self.left_frame.goback_buttons:
            button.bind(
                    '<Button-1>', self.move_button_pressed(button['text'])
                )
            button.bind('<ButtonRelease-1>', self.move_button_released)

    def move_speed_cmd(self, *args):
        self.left_frame.speed_frame.speed_display['text'] \
            = self.left_frame.move_speed.get()

    def move_button_pressed(self, kind):
        def inner(*e):
            cmd = kind
            if self.axis_status.index('1') == 1 or self.axis_status.index('1') == 5:
                if kind == '+':
                    cmd = '-'
                else:
                    cmd = '+'
            if self.is_fine_move.get():
                with OptoSigmaSRC101({'port': 'COM12'}) as o:
                    ##TODO: find good magnification
                    o.pulse_move(cmd, int(self.left_frame.move_speed.get())*160)
                self.left_frame.job = self.after(
                        100, self.move_button_pressed(kind)
                    )
            else:
                with OptoSigmaSRC101({'port': 'COM12'}) as o:
                    o.change_speed(int(self.left_frame.move_speed.get()))
                    o.jog_start(cmd)
            if self.is_continuous_move.get():
                for button in self.left_frame.goback_buttons \
                    + self.right_frame.switch_buttons:
                    button.state(['disabled'])
                self.stop_button.state(['!disabled'])
        return inner

    def move_button_released(self, e):
        if not self.is_continuous_move.get():
            self.stop_stage_move()

    def stop_stage_move(self):
        if self.is_fine_move.get():
            self.after_cancel(self.left_frame.job)
        else:
            with OptoSigmaSRC101({'port': 'COM12'}) as o:
                o.stop_move()
        for button in self.left_frame.goback_buttons \
            + self.right_frame.switch_buttons:
            button.state(['!disabled'])
        self.stop_button.state(['disabled'])

    def axis_button_cmd(self, kind):
        def inner():
            with KEISEEDS_RBIO2U({'port': 'COM11'}) as K:
                K.change_relay(kind)
            self.update_axis_button()
        return inner

    def update_axis_button(self):
        with KEISEEDS_RBIO2U({'port': 'COM11'}) as K:
            self.axis_status = K.ask_status()
        for button, status in zip(self.right_frame.switch_buttons, self.axis_status):
            button.configure(style = ('green' if int(status) else 'white') + '.TButton')
        

def main():
    master = Tk()
    master.bind('<Control-Key-c>', lambda e: master.quit())
    main_window(master).mainloop()

if __name__ == '__main__':
    main()