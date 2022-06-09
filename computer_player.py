from strategy import BasicStrategy, ComputerStrategyBuilder
from game_play_state import GamePlayState
from time import sleep


class ComputerPlayer:
    def __init__(self, computer_strategy_file_path: str, sign: str):
        loaded_strategy = ComputerStrategyBuilder(computer_strategy_file_path).load()
        self.sign = sign
        if(loaded_strategy) :
            print("Computer is playing with winning strategy.")
            self.strategy = loaded_strategy
        else:
            print("Computer is playing with basic strategy.")
            self.strategy = BasicStrategy()

    def next_move(self, board: GamePlayState.GameBoard) -> tuple[int, int]:
        sleep(1 / 3)
        return self.strategy.step(board, self.sign)
