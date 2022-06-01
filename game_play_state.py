from enum import Enum
import itertools


class GamePlayState:
    def __init__(self):
        self.turn: GamePlayState.GameTurn = GamePlayState.GameTurn.PLAYER
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

    class GameBoard:
        def __init__(self):
            self.board = [[None, None, None], [None, None, None], [None, None, None]]

        # TODO implement repr especially because we want to save-retrieve game state

        def __str__(self):
            def to_char(f):
                return f if f is not None else "-"

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

        def is_full(self):
            return all(itertools.chain(*self.board))

    def change_turn(self, turn: GameTurn):
        self.turn = turn

    def is_gameover(self):
        def does_someone_win():
            def signs_in_a_row():
                is_row1 = self.board[(0, 0)] == self.board[(0, 1)] \
                    and self.board[(0, 1)] == self.board[(0, 2)] \
                    and self.board[(0, 0)]  # Not all is None
                is_row2 = self.board[(1, 0)] == self.board[(1, 1)] \
                    and self.board[(1, 1)] == self.board[(1, 2)] \
                    and self.board[(1, 1)]  # Not all is None
                is_row3 = self.board[(2, 0)] == self.board[(2, 1)] \
                    and self.board[(2, 1)] == self.board[(2, 2)] \
                    and self.board[(2, 2)]  # Not all is None
                return is_row1 or is_row2 or is_row3

            def signs_in_a_column():
                is_col1 = self.board[(0, 0)] == self.board[(1, 0)] \
                    and self.board[(1, 0)] == self.board[(2, 0)] \
                    and self.board[(0, 0)]  # Not all is None
                is_col2 = self.board[(0, 1)] == self.board[(1, 1)] \
                    and self.board[(1, 1)] == self.board[(2, 1)] \
                    and self.board[(1, 1)]  # Not all is None
                is_col3 = self.board[(0, 2)] == self.board[(1, 2)] \
                    and self.board[(1, 2)] == self.board[(2, 2)] \
                    and self.board[(2, 2)]  # Not all is None
                return is_col1 or is_col2 or is_col3

            def signs_in_a_diagonal():
                is_d1 = self.board[(0, 0)] == self.board[(1, 1)] \
                    and self.board[(1, 1)] == self.board[(2, 2)] \
                    and self.board[(1, 1)]  # Not all is None
                is_d2 = self.board[(0, 2)] == self.board[(1, 1)] \
                    and self.board[(1, 1)] == self.board[(2, 0)] \
                    and self.board[(1, 1)]  # Not all is None
                return is_d1 or is_d2

            return signs_in_a_row() or signs_in_a_column() or signs_in_a_diagonal()

        return does_someone_win() or self.board.is_full()
