import abc
import pickle
from collections import deque
from enum import Enum
from itertools import groupby
from typing import NamedTuple, Optional, Generator
from pathlib import Path
from game_play_state import GamePlayState

EMPTY_SIGN = "-"
X_SIGN = "X"
O_SIGN = "O"

class Strategy(abc.ABC):
    @abc.abstractmethod
    def step(self, board: GamePlayState.GameBoard, sign: str) -> tuple[int,int]:
        pass


class BasicStrategy(Strategy):
    def step(self, board: GamePlayState.GameBoard, sign: str) -> tuple[int,int]:
        return next((move for (move, val) in board.items() if val is None))


class Winner(Enum):
    UNKNOWN = "UNKNOWN"
    X = "X"
    O = "O"
    BOTH = "BOTH"


class StrategyNode:
    def __init__(self, key: str, children: list[str], strategy: Winner = Winner.UNKNOWN):
        self.key: str = key
        self.children: list[str] = children
        self.strategy: Winner = strategy


class ComputerStrategy(Strategy):
    def __init__(self, data: dict[str, StrategyNode]): # TODO inject difficulty
        self.data : dict[str, StrategyNode] = data

    def step(self, board: GamePlayState.GameBoard, sign: str) -> tuple[int,int]:
        state = self.create_state_from_board(board)
        next_states = self.compute_next_states(state, sign)
        grouped = groupby([self.data[n] for n in next_states], lambda k: k.strategy)
        print(grouped)
        return (0,0) # TODO write logic for stepping

    def create_state_from_board(self, board : GamePlayState.GameBoard):
        signs = [board[(r,c)] for r in range(3) for c in range(3)]
        converted_signs = [x if x == X_SIGN or x == O_SIGN else EMPTY_SIGN for x in signs]
        return ''.join(converted_signs)

    def compute_next_states(self, state: str, sign: str) -> list[str]:
        next_states = []
        for i in range(9):
            if state[i] is EMPTY_SIGN:
                s = [*state]
                s[i] = sign
                next_states.append(''.join(s))
        return next_states



class ComputerStrategyBuilder:
    class GameOverState(NamedTuple):
        is_gameover: bool
        winner: Winner

    def __init__(self, computer_strategy_file_path: str):
        self.file = Path(computer_strategy_file_path)

    def build(self) -> Strategy:
        strategy = self.build_strategy()
        with open(self.file, "wb+") as f:
            pickle.dump(strategy, f)
        return strategy

    def load(self) -> Optional[ComputerStrategy]:
        if self.file.exists():
            with open(self.file, "rb+") as f:
                try:
                    return pickle.load(f)
                except Exception as e:
                    return None
        else:
            return None

    def build_strategy(self) -> ComputerStrategy:
        states_to_evaluate = [[EMPTY_SIGN] * 9]
        computed_state_graph = self.compute_states_with_children(states_to_evaluate)
        computed_strategy_graph = self.compute_strategy_with_children(computed_state_graph)
        return ComputerStrategy(computed_strategy_graph)

    def compute_states_with_children(self, states_to_evaluate: list[list[str]]) -> list[StrategyNode]:
        computed_states = []
        while len(states_to_evaluate):
            state = states_to_evaluate.pop()
            children = []
            sign = X_SIGN if state.count(X_SIGN) == state.count(O_SIGN) else O_SIGN
            state_key = ''.join(state)
            gameover_state = self.gameover_state(state_key)
            if not gameover_state.is_gameover:
                for i in range(0, 9):
                    s = state.copy()  # for not overwriting the state
                    if (s[i] == EMPTY_SIGN):
                        s[i] = sign
                        states_to_evaluate.append(s)
                        children.append(s)

            children_keys = [''.join(c) for c in children]
            computed_states.append(StrategyNode(state_key, children_keys, gameover_state.winner))
        return computed_states

    def compute_strategy_with_children(self, computed_state_graph: list[StrategyNode]):
        strategy_graph : dict[str, StrategyNode]= {g.key:g for g in computed_state_graph}
        nodes_to_calculate : deque[StrategyNode] = deque([strategy_graph[EMPTY_SIGN*9]])
        while len(nodes_to_calculate):
            node = nodes_to_calculate.popleft()
            if(node.strategy is not Winner.UNKNOWN): # the node has strategy already
                continue
            key = node.key
            children = strategy_graph[key].children
            children_strategies = [strategy_graph[c].strategy for c in children]

            if all([x is not Winner.UNKNOWN for x in children_strategies]):
                strategy = self.calculate_strategy_from_children(children_strategies)
                strategy_graph[key].strategy = strategy
            else:
                for c in children:
                    if c not in nodes_to_calculate:
                        nodes_to_calculate.appendleft(strategy_graph[c]) # calculating children of the current node must be done first
                if node not in nodes_to_calculate:
                    nodes_to_calculate.append(node) # Need to recalculate current node later
        return strategy_graph

    def calculate_strategy_from_children(self, children_strategies : list[Winner]):
        x_win_strategy = any([s is Winner.X for s in children_strategies])
        o_win_strategy = any([s is Winner.O for s in children_strategies])
        both_win_strategy = any([s is Winner.BOTH for s in children_strategies])

        if both_win_strategy:
            return Winner.BOTH
        if x_win_strategy and o_win_strategy:
            return Winner.BOTH
        if x_win_strategy:
            return Winner.X
        if o_win_strategy:
            return Winner.O
        return Winner.UNKNOWN

    def gameover_state(self, board: str) -> GameOverState:
        def board_is_full():
            return board.count(EMPTY_SIGN) == 0

        def has_sign_on_indexes(sign: str, i0: int, i1: int, i2 :int):
            return board[i0] == sign \
                and board[i1] == sign \
                    and board[i2] == sign

        def does_win(sign: str) -> str:
            def signs_in_a_row():
                return has_sign_on_indexes(sign, 0, 1, 2) \
                       or has_sign_on_indexes(sign, 3, 4, 5) \
                       or has_sign_on_indexes(sign, 6, 7, 8)

            def signs_in_a_column():
                return has_sign_on_indexes(sign, 0, 3, 6) \
                       or has_sign_on_indexes(sign, 1, 4, 7) \
                       or has_sign_on_indexes(sign, 2, 5, 8)

            def signs_in_a_diagonal():
                return has_sign_on_indexes(sign, 0, 4, 8) \
                       or has_sign_on_indexes(sign, 2, 4, 6)

            wins = signs_in_a_row() or signs_in_a_column() or signs_in_a_diagonal()
            return sign if wins else None

        if does_win(X_SIGN):
            return ComputerStrategyBuilder.GameOverState(True, Winner.X)
        if does_win(O_SIGN):
            return ComputerStrategyBuilder.GameOverState(True, Winner.O)
        if board_is_full():
            return ComputerStrategyBuilder.GameOverState(True, Winner.BOTH)
        return ComputerStrategyBuilder.GameOverState(False, Winner.UNKNOWN)

if (__name__ == '__main__'):
    ComputerStrategyBuilder("computer.strategy").build() # TODO extract magic constant