from tkinter import Tk, Button

class Game(Tk):
    def __init__(self):
        super().__init__()
        self.title("Tic tac toe")
        self.config(width=800, height=600)
        self.layout()

    def layout(self):
        indexes = [(r, c) for r in range(3) for c in range(3)]
        for r, c in indexes:
            text = f"Button ({r},{c})"
            btn = Button(self, text=text)
            btn.grid(row=r, column=c)
            
    def launch(self):
        self.mainloop()
