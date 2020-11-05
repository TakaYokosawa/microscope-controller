from tkinter import *
from tkinter import ttk

class UI_JogandSwitch(ttk.Frame):
    def __init__(self, master = None, goback_label = ['1', '-1'], switch_number = 5):
        super().__init__(master)
        self['borderwidth'] = 1
        self['relief'] = 'solid'
        self.pack(anchor = W, expand = 1, fill = BOTH, side = LEFT, padx = 5, pady = 5)

        self.label = ttk.Label(self, text='label', 
            font=('Helvetica', '20', 'bold')
        )
        self.label.pack()

        self.style = ttk.Style()
        self.style.configure('TButton', font = ('Helvetica', '20', 'bold'))

        self.left_frame = ttk.Frame(self, borderwidth=1, relief='solid')
        self.left_frame.pack(anchor = W, expand = 1, fill = BOTH, side = LEFT, padx = 5, pady = 5)

        self.left_frame.label = ttk.Label(self.left_frame, text='left', 
            font=('Helvetica', '20', 'bold')
        )
        self.left_frame.label.pack()

        self.left_frame.goback_button_kinds = goback_label
        self.left_frame.goback_buttons = [
                ttk.Button(
                    self.left_frame, text = i, 
                ) for i in self.left_frame.goback_button_kinds
            ]
        for button in self.left_frame.goback_buttons:
            button.pack(fill = BOTH, expand = 1, padx = 5, pady = 5)

        self.move_option_frame = ttk.Frame(self.left_frame)
        self.move_option_frame.pack()

        self.left_frame.speed_frame = ttk.LabelFrame(
                self.left_frame, text = 'speed'
            )
        self.left_frame.speed_frame.pack(
            fill = X, padx = 5, pady = 5
        )

        self.left_frame.speed_frame.speed_display = ttk.Label(
                self.left_frame.speed_frame, text = '1', width=5, anchor = E
            )
        self.left_frame.speed_frame.speed_display.pack(side = LEFT)

        self.left_frame.speed_frame.speed_scale = ttk.Scale(self.left_frame.speed_frame, 
                from_ = 1, to = 48, 
            )
        self.left_frame.speed_frame.speed_scale.pack(side = LEFT, fill = X, expand = 1, padx = 5)        

        self.right_frame = ttk.Frame(self, 
            borderwidth=1, relief='solid')
        self.right_frame.pack(anchor = E, expand = 1, fill = BOTH, side = RIGHT, padx = 5, pady = 5)
        self.right_frame.label = ttk.Label(
                self.right_frame, text='right', font=('Helvetica', '20', 'bold'), justify = CENTER
            )
        self.right_frame.label.pack()
        self.right_label_frame = ttk.Frame(self.right_frame)
        self.right_label_frame.pack(fill = BOTH)
        self.right_frame.button_frame = ttk.Frame(self.right_frame)
        self.right_frame.button_frame.pack()

        self.right_frame.switch_buttons = [
                ttk.Button(
                    self.right_frame.button_frame, text = i, width = 6 
                ) for i in range(switch_number)
            ]
        for i, button in enumerate(self.right_frame.switch_buttons):
            button.grid(column = i//5, row = i%5, 
                padx = 5, pady = 5)            

def main():
    master = Tk()
    master.bind('<Control-Key-c>', lambda e: master.quit())
    Microscope_main = UI_JogandSwitch(master)
    Microscope_main.mainloop()

if __name__ == '__main__':
    main()