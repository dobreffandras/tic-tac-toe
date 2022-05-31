from enum import Enum
from collections.abc import Callable


class GameState(Enum):
    START = "START"
    PLAYING = "PLAYING"
    GAMEOVER = "GAMEOVER"


class GameEngine:
    def __init__(self, gamestate_listener: Callable[[GameState], None]):
        self.player_sign = "X" # TODO Player may choose to be Player2 instead later
        self.listener = gamestate_listener
        self.playing_state = GamePlayState()

    def launch(self):
        self.listener(GameState.START)

    def start_playing(self):
        self.listener(GameState.PLAYING)

    def player_chooses(self, r, c):
        print("Player Chooses", r, c)
        self.playing_state.add_sign_to((r,c), self.player_sign)
        self.playing_state_listener(self.playing_state)

    def connect_playing_state_change_handler(self, playing_state_listener : Callable[[object], None]):
        self.playing_state_listener = playing_state_listener


class GamePlayState:
    def __init__(self):
        self.turn : GamePlayState.GameTurn = GamePlayState.GameTurn.PLAYER # TODO Player may choose to be Player2 instead later
        self.board : GamePlayState.GameBoard = GamePlayState.GameBoard()

    def __str__(self):
        return """\n-------
ON TURN: {}
BOARD:
{}
-----
        """.format(self.turn, self.board)

    def add_sign_to(self, coord: tuple[int, int], player_sign):
        self.board[coord] = player_sign

    class GameTurn(Enum):
        PLAYER = "PLAYER"
        COMPUTER = "COMPUTER"

    class GameBoard():
        def __init__(self):
            self.board = [[None,None,None], [None,None,None], [None,None,None]]

        # TODO implement repr especially because we want to save-retrieve game state

        def __str__(self):
            def to_char(b):
                return b if b is not None else "-"

            b = {(r,c):to_char(self.board[r][c]) for r in range(3) for c in range(3)}

            return f"-------\n\
|{b[(0, 0)]}|{b[(0, 1)]}|{b[(0, 2)]}|\n\
|{b[(1, 0)]}|{b[(1, 1)]}|{b[(1, 2)]}|\n\
|{b[(2, 0)]}|{b[(2, 1)]}|{b[(2, 2)]}|\n\
-------"

        def __setitem__(self, key: tuple[int, int], value):
            self.board[key[0]][key[1]] = value