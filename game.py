from tkinter import Tk

class Game(Tk):
    def __init__(self):
        super().__init__()
        self.title("Tic tac toe")
        self.config(width=800, height=600)
    def launch(self):
        self.mainloop()
