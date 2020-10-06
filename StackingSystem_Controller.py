from tkinter import *
from tkinter import ttk

from Microscope_Controller import main_window as Microscope_main
from Stage_Controller import main_window as Stage_main

class StackingMainWindow(ttk.Frame):
    def __init__(self, master = None):
        super().__init__(master)
        self.master.title('stacking system')
        self.pack()
        Microscope_main(self)
        Stage_main(self)

def main():
    master = Tk()
    master.bind('<Control-Key-c>', lambda e: master.quit())
    main_window = StackingMainWindow(master)
    main_window.mainloop()

if __name__ == '__main__':
    main()