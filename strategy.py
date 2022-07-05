import abc
import pickle
from collections import deque
from enum import Enum
from random import choice
from typing import NamedTuple, Optional
from pathlib import Path
from game_play_state import GamePlayState

FILENAME = "computer.strategy"

EMPTY_SIGN = "-"
X_SIGN = "X"
O_SIGN = "O"


class Difficulty(Enum):
    EASY = 1
    MEDIUM = 2
    HARD = 3


class Strategy(abc.ABC):
    """
    This is the base class for the different strategies used by the ComputerPlayer
    """
    @abc.abstractmethod
    def step(self, board: GamePlayState.GameBoard, sign: str, difficulty: Difficulty) -> tuple[int, int]:
        pass


class BasicStrategy(Strategy):
    """
    The basic strategy will always yield the next available field as the step of the computer opponent
    """
    def step(self, board: GamePlayState.GameBoard, sign: str, difficulty: Difficulty) -> tuple[int, int]:
        return next((move for (move, val) in board.items() if val is None))


class Winner(Enum):
    """
    This Enum indicates which player can win from the current board setup.
    """
    UNKNOWN = "UNKNOWN"
    X = "X"
    O = "O"
    BOTH = "BOTH"


class StrategyNode:
    """
    This class represents a node in the gamestate graph. (e.g. the initial node is the empty field with the X being on turn.)
    The children of a node are the gamestates that are reachable from the
    current one. (e.g. from the initial node all nodes that have only one X are children.)
    The key is the string representation of the board. The strategy represents which player can win from this state.
    """
    def __init__(self, key: str, children: list[str], on_turn: str, strategy: Winner = Winner.UNKNOWN):
        self.key: str = key
        self.children: list[str] = children
        self.on_turn = on_turn
        self.strategy: Winner = strategy


class ComputerStrategy(Strategy):
    """
    This strategy will choose step based on the strategy graph (data) and difficulty.
    """
    def __init__(self, data: dict[str, StrategyNode]):
        self.data: dict[str, StrategyNode] = data

    def step(self, board: GamePlayState.GameBoard, sign: str, difficulty: Difficulty) -> tuple[int, int]:
        """
        This method will choose the next step of the computer player based on the current board, the strategy graph and difficulty.
        The difficulty defines how the next step will be chosen. On HARD the children are filtered only for the best possible scenario.
        On MEDIUM difficulty natural choices are also possible. On EASY the strategy chooses actually randomly.
        """
        def choose_from_possibilities(*, best, natural, worst):
            if len(best):
                return choice(best)
            elif len(natural):
                return choice(natural)
            else:
                return choice(worst)

        state = self.create_state_from_board(board)
        next_states = self.compute_next_states(state, sign)
        x_winners = [next_states[n] for n in next_states if self.data[n].strategy == Winner.X]
        o_winners = [next_states[n] for n in next_states if self.data[n].strategy == Winner.O]
        both_winners = [next_states[n] for n in next_states if self.data[n].strategy == Winner.BOTH]

        if sign == X_SIGN:
            if difficulty == Difficulty.HARD:
                return choose_from_possibilities(best=x_winners, natural=both_winners, worst=o_winners)
            elif difficulty == Difficulty.MEDIUM:
                not_loosing = [*x_winners, *both_winners, *o_winners]
                return choose_from_possibilities(best=[], natural=not_loosing, worst=[])
            else:
                return choose_from_possibilities(best=o_winners, natural=both_winners, worst=x_winners)

        if sign == O_SIGN:
            if difficulty == Difficulty.HARD:
                return choose_from_possibilities(best=o_winners, natural=both_winners, worst=x_winners)
            elif difficulty == Difficulty.MEDIUM:
                not_loosing = [*x_winners, *both_winners, *o_winners]
                return choose_from_possibilities(best=[], natural=not_loosing, worst=[])
            else:
                return choose_from_possibilities(best=x_winners, natural=both_winners, worst=o_winners)

    def create_state_from_board(self, board: GamePlayState.GameBoard):
        signs = [board[(r, c)] for r in range(3) for c in range(3)]
        converted_signs = [x if x == X_SIGN or x == O_SIGN else EMPTY_SIGN for x in signs]
        return ''.join(converted_signs)

    def compute_next_states(self, state: str, sign: str) -> dict[str, tuple[int, int]]:
        next_states = {}
        for i in range(9):
            if state[i] is EMPTY_SIGN:
                s = [*state]
                s[i] = sign
                index = divmod(i, 3)
                next_states[''.join(s)] = index
        return next_states


class ComputerStrategyBuilder:
    """
    This class can build up, save and load a strategy graph to/from file.
    """
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
                except:
                    return None
        else:
            return None

    def build_strategy(self) -> ComputerStrategy:
        """
        This method builds up the strategy graph
        :return: the strategy graph
        """
        states_to_evaluate = [[EMPTY_SIGN] * 9]
        computed_state_graph = self.compute_states_with_children(states_to_evaluate)
        computed_strategy_graph = self.compute_strategy_with_children(computed_state_graph)
        return ComputerStrategy(computed_strategy_graph)

    def compute_states_with_children(self, states_to_evaluate: list[list[str]]) -> list[StrategyNode]:
        """
        This method creates a list of strategy nodes which represent a possible state of the game.

        The algorithm pops one node from a queue and creates its children which are added to the queue as well.
        "game over" nodes are marked with the winner.
        The algorithm stops when queue becomes empty.
        :param states_to_evaluate: The list of initial nodes. This should be a list with the initial node.
        """
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
                    if s[i] == EMPTY_SIGN:
                        s[i] = sign
                        states_to_evaluate.append(s)
                        children.append(s)

            children_keys = [''.join(c) for c in children]
            computed_states.append(StrategyNode(state_key, children_keys, sign, gameover_state.winner))
        return computed_states

    def compute_strategy_with_children(self, computed_state_graph: list[StrategyNode]):
        """
        This method calculates the potential winners in the intermediate game states of the state graph
        The method uses a deque to keep track of the nodes to be evaluated. If a node has UNKNOWN strategy
        the strategy is calculated from its children (if they are already have). If the children also require calculation
        they are pushed to the deque.
        The algorithm stops once the deque is empty.
        :param computed_state_graph: the already built state graph that only needs strategy evaluation in the nodes.
        :return: A state graph that has an evaluated strategy for all nodes.
        """
        strategy_graph: dict[str, StrategyNode] = {g.key: g for g in computed_state_graph}
        nodes_to_calculate: deque[StrategyNode] = deque([strategy_graph[EMPTY_SIGN * 9]])
        while len(nodes_to_calculate):
            node = nodes_to_calculate.popleft()
            if node.strategy is not Winner.UNKNOWN:  # the node has strategy already
                continue
            key = node.key
            children = strategy_graph[key].children
            children_strategies = [strategy_graph[c].strategy for c in children]

            if all([x is not Winner.UNKNOWN for x in children_strategies]):
                strategy = self.calculate_strategy_from_children(children_strategies, node.on_turn)
                strategy_graph[key].strategy = strategy
            else:
                for c in children:
                    if c not in nodes_to_calculate:
                        nodes_to_calculate.appendleft(
                            strategy_graph[c])  # calculating children of the current node must be done first
                if node not in nodes_to_calculate:
                    nodes_to_calculate.append(node)  # Need to recalculate current node later
        return strategy_graph

    def calculate_strategy_from_children(self, children_strategies: list[Winner], on_turn: str):
        x_win_strategy = any([s is Winner.X for s in children_strategies])
        o_win_strategy = any([s is Winner.O for s in children_strategies])
        both_win_strategy = any([s is Winner.BOTH for s in children_strategies])

        if not x_win_strategy and not o_win_strategy:
            return Winner.BOTH
        if x_win_strategy and o_win_strategy:
            if on_turn == X_SIGN:
                return Winner.X
            if on_turn == O_SIGN:
                return Winner.O
        if x_win_strategy and not o_win_strategy:
            if on_turn == O_SIGN and both_win_strategy:
                return Winner.BOTH
            else:
                return Winner.X
        if o_win_strategy and not x_win_strategy:
            if on_turn == X_SIGN and both_win_strategy:
                return Winner.BOTH
            else:
                return Winner.O

    def gameover_state(self, board: str) -> GameOverState:
        """
        Determines whether the current board is a game over state. (either a player wins or the board is full)
        :return A GameOverState that has boolean (whether is a gameover state or not) and an optional winner.
        """
        def board_is_full():
            return board.count(EMPTY_SIGN) == 0

        def has_sign_on_indexes(sign: str, i0: int, i1: int, i2: int):
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


if __name__ == '__main__':
    ComputerStrategyBuilder(FILENAME).build()
