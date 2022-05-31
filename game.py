from game_engine import GameEngine, GameState
from tkinter import Tk, Button


class Game(Tk):
    def __init__(self):
        super().__init__()
        self.game_engine = GameEngine(self.gamestate_change_handler)
        self.title("Tic tac toe")
        self.config(width=800, height=600)

    def gamestate_change_handler(self, game_state: GameState):
        for child in self.winfo_children():
            child.destroy()

        if game_state == GameState.START:
            Game.Start(self, self.game_engine)
        if game_state == GameState.PLAYING:
            Game.Playing(self)

    def launch(self):
        self.game_engine.launch()
        self.mainloop()

    class Playing:
        def __init__(self, tk_root):
            self.tk_root = tk_root
            self.playfield_buttons = {}
            self.indexes = [(r, c) for r in range(3) for c in range(3)]
            self.setup_controls()
            self.layout_controls()

        def setup_controls(self):
            for r, c in self.indexes:
                text = f"Button ({r},{c})"
                btn = Button(self.tk_root, text=text, command=self.create_button_command(r, c))
                self.playfield_buttons[(r, c)] = btn

        def create_button_command(self, r, c):
            def command():
                print(r, c)

            return command

        def layout_controls(self):
            for key, btn in self.playfield_buttons.items():
                r, c = key
                btn.grid(row=r, column=c)

    class Start:
        def __init__(self, tk_root, engine: GameEngine):
            self.tk_root = tk_root
            self.engine = engine
            self.setup_controls()
            self.layout_controls()

        def setup_controls(self):
            self.game_start_button = Button(self.tk_root,
                                            text="Start Game",
                                            command=self.engine.start_playing)

        def layout_controls(self):
            self.game_start_button.pack()