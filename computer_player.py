from time import sleep
from game_play_state import GamePlayState
from strategy import Strategy


class ComputerPlayer:
    def __init__(self, strategy: Strategy, sign: str):
        self.sign = sign
        self.strategy = strategy


    def next_move(self, board: GamePlayState.GameBoard) -> tuple[int, int]:
        sleep(1 / 3)
        return self.strategy.step(board, self.sign)
