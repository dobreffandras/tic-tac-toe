from strategy import BasicStrategyBuilder
from game_play_state import GamePlayState
from time import sleep


class ComputerPlayer:
    def __init__(self, computer_strategy_file_path: str):
        # TODO We will create a ComputerStrategyBuilder with the path. The basic doesn't need any
        self.strategy = BasicStrategyBuilder().build()

    def next_move(self, board: GamePlayState.GameBoard) -> tuple[int, int]:
        sleep(1 / 3)
        return self.strategy.step(board)
