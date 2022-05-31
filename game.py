from tkinter import Tk, Button

class Game(Tk):
    def __init__(self):
        super().__init__()
        self.playfield_buttons = {}
        self.indexes = [(r, c) for r in range(3) for c in range(3)]
        self.title("Tic tac toe")
        self.config(width=800, height=600)
        self.setup_controls()
        self.layout_controls()

    def setup_controls(self):
        for r, c in self.indexes:
            text = f"Button ({r},{c})"
            btn = Button(self, text=text, command=self.create_button_command(r, c))
            self.playfield_buttons[(r,c)] = btn
    
    def create_button_command(self, r, c):
        def command():
            print(r,c)
        return command
        
    def layout_controls(self):
        for key, btn in self.playfield_buttons.items():
            r, c = key
            btn.grid(row=r, column=c)
            
    def launch(self):
        self.mainloop()
