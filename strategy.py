import abc
from collections import deque
from typing import Optional
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
                f.write(repr(strategy.data))
            return strategy

    def build_strategy(self) -> ComputerStrategy:
        states_to_evaluate = [["-"]*9]
        computed_state_graph = self.compute_states_with_children(states_to_evaluate)
        computed_strategy_graph = self.compute_strategy_with_children(computed_state_graph)
        strat = ComputerStrategy()
        strat.data = {k[0]:f"(s={k[1].strategy} c={k[1].children}" for k in computed_strategy_graph.items()}
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

    def compute_strategy_with_children(self, computed_state_graph):
        class StrategyNode: # TODO namedtuple
            def __init__(self, key:str, children: list[str]):
                self.key : str = key
                self.children: list[str] = children
                self.strategy : Optional[list[str]] = None

        strategy_graph : dict[str, StrategyNode]= {g["key"]:StrategyNode(g["key"], g["children"]) for g in computed_state_graph}
        nodes_to_calculate : deque[StrategyNode] = deque([strategy_graph["-"*9]])
        while len(nodes_to_calculate):
            node = nodes_to_calculate.popleft()
            key = node.key
            children = strategy_graph[key].children
            children_strategies = [strategy_graph[c].strategy for c in children]
            if winner_sign := self.gameover_state(key):
                strategy_graph[key].strategy = [winner_sign]
            elif all(children_strategies):
                strategy = self.calculate_strategy_from_children(children_strategies)
                strategy_graph[key].strategy = strategy
            else:
                for c in children:
                    nodes_to_calculate.appendleft(strategy_graph[c]) # calculating children of the current node must be done first
                nodes_to_calculate.append(node) # Need to recalculate current node later
        return strategy_graph

    def calculate_strategy_from_children(self, children_strategies):
        x_win_strategy = any(["X" in s for s in children_strategies])
        o_win_strategy = any(["O" in s for s in children_strategies])
        strategy = []
        if x_win_strategy:
            strategy.append("X")
        if o_win_strategy:
            strategy.append("O")
        return strategy

    def gameover_state(self, board: str) -> str:
        return board.count("-") == 0 and "X" # All full boards are winning states for X for now


ComputerStrategyBuilder("local.strategy").build() # Just for testing purposes