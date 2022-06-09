from time import sleep
from game_play_state import GamePlayState
from strategy import Strategy, Difficulty


class ComputerPlayer:
    def __init__(self, strategy: Strategy, sign: str, difficulty: Difficulty):
        self.sign = sign
        self.strategy = strategy
        self.difficulty = difficulty


    def next_move(self, board: GamePlayState.GameBoard) -> tuple[int, int]:
        sleep(1 / 3)
        return self.strategy.step(board, self.sign, self.difficulty)
