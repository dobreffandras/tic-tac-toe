import abc
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


class ComputerStrategyBuilder:
    def build(self) -> Strategy:
        pass
