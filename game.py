from game_engine import GameEngine, GameState
from game_play_state import GamePlayState, GameTurn
from tkinter import Tk, Frame, Label, Button, Radiobutton, PhotoImage, StringVar, NORMAL, DISABLED, CENTER
import threading


class Game(Tk):
    def __init__(self):
        super().__init__()
        self.game_engine = GameEngine(self.gamestate_change_handler)
        self.title("Tic tac toe")
        self.geometry("250x320")

    def gamestate_change_handler(self, game_state: GameState):
        for child in self.winfo_children():
            child.destroy()

        if game_state == GameState.START:
            Game.Start(self, self.game_engine)
        if game_state == GameState.PLAYING:
            Game.Playing(self, self.game_engine)
        if game_state == GameState.GAMEOVER:
            Game.GameOver(self, self.game_engine)

    def launch(self):
        self.game_engine.launch()
        self.mainloop()

    class Playing:

        turn_indicator_config = {
            "player": dict(text="It's your turn.", font=("Courier", "12", "bold"), bg="#0F0"),
            "computer": dict(text="Opponent is on turn.", font=("Courier", "12", "bold"), bg="#FFA500")
        }

        def __init__(self, tk_root, engine: GameEngine):
            self.tk_root = tk_root
            self.engine = engine
            self.engine.connect_playing_state_change_handler(self.playing_state_changed)
            self.playfield_buttons = {}
            self.indexes = [(r, c) for r in range(3) for c in range(3)]
            self.images = {}
            self.playfield = None
            self.on_turn_text_field = None
            self.setup_controls()
            self.layout_controls()

        def setup_controls(self):
            self.images = {
                "CIRCLE": PhotoImage(file=r"images\circle.png", width=64, height=64),
                "CROSS": PhotoImage(file=r"images\cross.png", width=64, height=64),
                "EMPTY": PhotoImage(file=r"images\empty.png", width=64, height=64)
            }
            state = self.engine.playing_state
            is_player_on_turn = state.turn is GameTurn.PLAYER
            btn_state = NORMAL if is_player_on_turn else DISABLED

            self.playfield = Frame(self.tk_root)
            for r, c in self.indexes:
                btn = Button(self.playfield,
                             image=self.images["EMPTY"],
                             state=btn_state,
                             command=self.create_button_command(r, c))
                self.playfield_buttons[(r, c)] = btn

            on_turn_config = self.turn_indicator_config["player" if is_player_on_turn else "computer"]
            self.on_turn_text_field = Label(self.tk_root, **on_turn_config)

        def create_button_command(self, r, c):
            def command():
                print("Player Chooses", r, c)
                self.engine.player_chooses(r, c)

            t = threading.Thread(target=command)
            return lambda: t.start()

        def layout_controls(self):
            for key, btn in self.playfield_buttons.items():
                r, c = key
                btn.grid(row=r, column=c)

            self.playfield.pack(padx=20, pady=20)
            self.on_turn_text_field.pack(ipadx=3, ipady=3)

        def playing_state_changed(self, state: GamePlayState):
            print("New State:", str(state))
            is_player_on_turn = state.turn is GameTurn.PLAYER
            on_turn_config = self.turn_indicator_config["player" if is_player_on_turn else "computer"]
            self.on_turn_text_field.config(**on_turn_config)
            for key, btn in self.playfield_buttons.items():
                item = state.board[key]
                is_btn_clickable = is_player_on_turn and item is None
                btn_state = NORMAL if is_btn_clickable else DISABLED
                btn_image = "CROSS" if item == "X" else "CIRCLE" if item == "O" else "EMPTY"
                btn.config(image=self.images[btn_image], state=btn_state)

    class Start:
        def __init__(self, tk_root, engine: GameEngine):
            self.player_sign_tkvar = StringVar(value="X")
            self.frame = None
            self.welcome_label = None
            self.note_label = None
            self.sign_chooser_buttons = []
            self.game_start_button = None
            self.tk_root = tk_root
            self.engine = engine
            self.setup_controls()
            self.layout_controls()

        def setup_controls(self):
            self.frame = Frame(self.tk_root)
            self.welcome_label = Label(self.frame, text="Choose a sign:", font=("Courier", "12"))
            self.sign_chooser_buttons = [
                Radiobutton(self.frame, text="X", value="X", variable=self.player_sign_tkvar),
                Radiobutton(self.frame, text="O", value="O", variable=self.player_sign_tkvar)
            ]
            self.note_label = Label(self.frame, text="Note: X is the first player", font=("Arial", "10", "italic"))
            self.game_start_button = Button(self.frame,
                                            text="Start Game",
                                            command=threading.Thread(target=lambda :self.engine.start_playing(self.player_sign_tkvar.get())).start)

        def layout_controls(self):
            self.frame.place(anchor=CENTER, relx=0.5, rely=0.5)
            self.welcome_label.pack()
            self.sign_chooser_buttons[0].pack(pady=(5, 0))
            self.sign_chooser_buttons[1].pack(pady=(0, 5))
            self.note_label.pack(pady=(5, 15))
            self.game_start_button.pack()

    class GameOver:
        def __init__(self, tk_root, engine: GameEngine):
            self.game_over_label = None
            self.tk_root = tk_root
            self.images = {}
            self.playfield = None
            self.playfield_buttons = {}
            self.restart_button = None
            self.engine = engine
            self.setup_controls()
            self.layout_controls()

        def setup_controls(self):
            self.images = {  # TODO move to Game classvar
                "CIRCLE": PhotoImage(file=r"images\circle.png", width=64, height=64),
                "CROSS": PhotoImage(file=r"images\cross.png", width=64, height=64),
                "EMPTY": PhotoImage(file=r"images\empty.png", width=64, height=64)
            }

            self.playfield = Frame(self.tk_root)

            for ((r, c), item) in self.engine.gameover_state["board"]:
                btn_image = "CROSS" if item == "X" else "CIRCLE" if item == "O" else "EMPTY"
                btn = Button(self.playfield,
                             image=self.images[btn_image],
                             state=DISABLED,
                             command=self.none_command)  # somehow tkinter button breaks without a command
                self.playfield_buttons[(r, c)] = btn
            winner_sign = self.engine.gameover_state["winner"]
            game_over_text = f"Game over. {winner_sign} wins." if winner_sign else "Game over. It's a tie."
            self.game_over_label = Label(self.tk_root, font=("Courier", "12", "bold"), text=game_over_text)
            self.restart_button = Button(self.tk_root, text="Restart", command=self.engine.restart)

        def none_command(self): ...

        def layout_controls(self):
            self.playfield.pack(padx=20, pady=20)
            for key, btn in self.playfield_buttons.items():
                r, c = key
                btn.grid(row=r, column=c)

            self.game_over_label.pack(ipadx=3, ipady=3)
            self.restart_button.pack()
