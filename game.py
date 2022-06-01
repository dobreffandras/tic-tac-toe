from game_engine import GameEngine, GameState
from game_play_state import GamePlayState
from tkinter import Tk, Frame, Label, Button, NORMAL, DISABLED


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
            Game.Playing(self, self.game_engine)

    def launch(self):
        self.game_engine.launch()
        self.mainloop()

    class Playing:
        def __init__(self, tk_root, engine: GameEngine):
            self.tk_root = tk_root
            self.engine = engine
            self.engine.connect_playing_state_change_handler(self.playing_state_changed)
            self.playfield_buttons = {}
            self.indexes = [(r, c) for r in range(3) for c in range(3)]
            self.setup_controls()
            self.layout_controls()

        def setup_controls(self):
            self.playfield = Frame(self.tk_root)
            for r, c in self.indexes:
                btn = Button(self.playfield, text="-", command=self.create_button_command(r, c))
                self.playfield_buttons[(r, c)] = btn
            self.on_turn_text_field = Label(self.tk_root, text="Your turn")

        def create_button_command(self, r, c):
            def command():
                print("Player Chooses", r, c)
                self.engine.player_chooses(r, c)

            return command

        def layout_controls(self):
            self.playfield.pack()
            self.on_turn_text_field.pack()
            for key, btn in self.playfield_buttons.items():
                r, c = key
                btn.grid(row=r, column=c)

        def playing_state_changed(self, state: GamePlayState):
            print("New State:", str(state))
            is_player_on_turn = state.turn is GamePlayState.GameTurn.PLAYER
            for key, btn in self.playfield_buttons.items():
                item = state.board[key]
                is_btn_clickable = is_player_on_turn and item is None
                btn_state = NORMAL if is_btn_clickable else DISABLED
                btn_text = item if item else "-"
                btn.config(text=btn_text, state=btn_state)

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
