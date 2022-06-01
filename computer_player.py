from game_play_state import GamePlayState
from time import sleep


class ComputerPlayer:
    def next_move(self, board: GamePlayState.GameBoard) -> tuple[int, int]:
        sleep(1/3)
        return next((move for (move, val) in board.items() if val is None))