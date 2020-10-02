from tkinter import *
from tkinter import ttk

class Ui_MicroscopeMainWindow(object):
    def __init__(self):
        self.root = Tk()
        self.root.title("microscope controller")
        # self.root.geometry("400x400")
        self.root.bind('<Control-Key-c>', lambda e: self.root.quit())

        self.style = ttk.Style()
        self.style.configure('TButton', font = ('Helvetica', '20', 'bold'))

        self.root.focus_frame = ttk.Frame(self.root, borderwidth=1, relief='solid')
        self.root.focus_frame.pack(anchor = W, expand = 1, fill = BOTH, side = LEFT, padx = 5, pady = 5)

        ttk.Label(self.root.focus_frame, text='focus', 
            font=('Helvetica', '20', 'bold')
        ).pack()

        self.root.focus_frame.focus_speed_exp = DoubleVar(value= 0.0)
        self.root.focus_frame.focus_speed = IntVar(value= 1)
        self.root.focus_frame.focus_speed_field = StringVar(value= '')

        self.root.focus_frame.focus_button_kinds = ['U', 'D']
        self.root.focus_frame.focus_buttons = [
                ttk.Button(
                    self.root.focus_frame, text = i, 
                ) for i in self.root.focus_frame.focus_button_kinds
            ]

        for button in self.root.focus_frame.focus_buttons:
            button.pack(fill = BOTH, expand = 1, padx = 5, pady = 5)

        self.root.focus_frame.focus_speed_frame = ttk.LabelFrame(
                self.root.focus_frame, text = 'focus speed'
            )
        self.root.focus_frame.focus_speed_frame.pack(
            fill = X, padx = 5, pady = 5
        )

        self.root.focus_frame.focus_speed_frame.focus_speed_display = ttk.Label(
                self.root.focus_frame.focus_speed_frame, text = '1', width=5, anchor = E
            )
        self.root.focus_frame.focus_speed_frame.focus_speed_display.pack(side = LEFT)

        self.root.focus_frame.focus_speed_frame.val_cmd = self.root.focus_frame.focus_speed_frame.register(
                lambda P: True
            )
        ttk.Entry(self.root.focus_frame.focus_speed_frame,
                textvariable = self.root.focus_frame.focus_speed_field, 
                validatecommand = (self.root.focus_frame.focus_speed_frame.val_cmd, '%P'),
                validate = 'key',
                width=5
            ).pack(side = RIGHT)

        self.root.objective_frame = ttk.Frame(self.root, 
            borderwidth=1, relief='solid')
        self.root.objective_frame.pack(anchor = E, expand = 1, fill = BOTH, side = RIGHT, padx = 5, pady = 5)
        ttk.Label(
                self.root.objective_frame, text='objective', font=('Helvetica', '20', 'bold')
            ).pack()

def main():
    Microscope_main = Ui_MicroscopeMainWindow()
    Microscope_main.root.mainloop()

if __name__ == '__main__':
    main()