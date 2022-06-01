from game_play_state import GamePlayState


class ComputerPlayer:
    def next_move(self, board: GamePlayState.GameBoard) -> tuple[int, int]:
        return next((move for (move, val) in board.items() if val is None))