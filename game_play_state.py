from enum import Enum


class GamePlayState:
    def __init__(self):
        self.turn: GamePlayState.GameTurn = GamePlayState.GameTurn.PLAYER  # TODO Player may choose to be Player2 instead later
        self.board: GamePlayState.GameBoard = GamePlayState.GameBoard()

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
            self.board = [[None, None, None], [None, None, None], [None, None, None]]

        # TODO implement repr especially because we want to save-retrieve game state

        def __str__(self):
            def to_char(b):
                return b if b is not None else "-"

            b = {(r, c): to_char(x) for ((r, c), x) in self.items()}

            return f"-------\n\
|{b[(0, 0)]}|{b[(0, 1)]}|{b[(0, 2)]}|\n\
|{b[(1, 0)]}|{b[(1, 1)]}|{b[(1, 2)]}|\n\
|{b[(2, 0)]}|{b[(2, 1)]}|{b[(2, 2)]}|\n\
-------"

        def __getitem__(self, key: tuple[int, int]):
            return self.board[key[0]][key[1]]

        def __setitem__(self, key: tuple[int, int], value):
            self.board[key[0]][key[1]] = value

        def items(self):
            return [((r, c), self.board[r][c]) for r in range(3) for c in range(3)]

    def change_turn(self, turn: GameTurn):
        self.turn = turn
