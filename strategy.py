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
    def __init__(self):
        self.data = []

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
            with open(self.file, "w+") as f:
                f.write(repr(strategy.data[0:500]))
            return strategy

    def build_strategy(self) -> ComputerStrategy:
        states_to_evaluate = [["-"]*9]
        computed_state_graph = self.compute_states_with_children(states_to_evaluate)

        strat = ComputerStrategy()
        strat.data = computed_state_graph
        return strat

    def compute_states_with_children(self, states_to_evaluate):
        computed_states = []
        while len(states_to_evaluate):
            state = states_to_evaluate.pop()
            children = []
            sign = "X" if state.count("X") == state.count("O") else "O"
            for i in range(0, 9):
                s = state.copy()  # for not overwriting the state
                if (s[i] == "-"):
                    s[i] = sign
                    states_to_evaluate.append(s)
                    children.append(s)

            computed_states.append({"key": ''.join(state), "children": [''.join(c) for c in children]})
        return computed_states


ComputerStrategyBuilder("local.strategy").build() # Just for testing purposes