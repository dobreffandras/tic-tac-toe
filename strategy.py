import abc
from pathlib import Path

from game_play_state import GamePlayState


class Strategy(abc.ABC):
    @abc.abstractmethod
    def step(self, board: GamePlayState.GameBoard) -> tuple[int,int]:
        pass


class BasicStrategy(Strategy):
    def step(self, board: GamePlayState.GameBoard) -> tuple[int,int]:
        return next((move for (move, val) in board.items() if val is None))


class BasicStrategyBuilder:
    def build(self) -> Strategy:
        return BasicStrategy()

class ComputerStrategy(Strategy):
    def step(self, board: GamePlayState.GameBoard) -> tuple[int,int]:
        return (0,0) # TODO write logic for stepping

class ComputerStrategyBuilder:
    def __init__(self, computer_strategy_file_path: str):
        self.file = Path(computer_strategy_file_path)

    def build(self) -> Strategy:
        if self.file.exists():
            # TODO load strategy from file
            ...
        else:
            strategy = self.build_strategy()
            # TODO save strategy to file
            return strategy

    def build_strategy(self) -> Strategy:
        pass
