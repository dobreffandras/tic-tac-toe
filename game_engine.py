from enum import Enum
from collections.abc import Callable
from computer_player import ComputerPlayer
from game_play_state import GamePlayState


class GameState(Enum):
    START = "START"
    PLAYING = "PLAYING"
    GAMEOVER = "GAMEOVER"


class GameEngine:
    def __init__(self, gamestate_listener: Callable[[GameState], None]):
        self.playing_state_listener = None
        self.player_sign = "X"  # TODO Player may choose to be Player2 instead later
        self.computer_player_sign = "O"
        self.listener = gamestate_listener
        self.playing_state = GamePlayState()
        self.gameover_state = None
        self.computer_player = ComputerPlayer()

    def launch(self):
        self.listener(GameState.START)

    def start_playing(self):
        self.listener(GameState.PLAYING)

    def player_chooses(self, r, c):
        # Receive players move
        self.playing_state.add_sign_to((r, c), self.player_sign)
        if winner_sign := self.playing_state.is_gameover():
            self.gameover_state = {"board": self.playing_state.board.items(), "winner": winner_sign}
            self.listener(GameState.GAMEOVER)
            return
        else:
            self.playing_state_listener(self.playing_state)

        # Change active player to computer
        self.playing_state.change_turn(GamePlayState.GameTurn.COMPUTER)
        self.playing_state_listener(self.playing_state)

        # Receive computers move and change active player to player
        (c_r, c_c) = self.computer_player.next_move(self.playing_state.board)
        self.playing_state.add_sign_to((c_r, c_c), self.computer_player_sign)
        if winner_sign := self.playing_state.is_gameover():
            self.gameover_state = {"board": self.playing_state.board.items(), "winner": winner_sign}
            self.listener(GameState.GAMEOVER)
            return
        else:
            self.playing_state.change_turn(GamePlayState.GameTurn.PLAYER)
            self.playing_state_listener(self.playing_state)

    def connect_playing_state_change_handler(self, playing_state_listener: Callable[[GamePlayState], None]):
        self.playing_state_listener = playing_state_listener

    def restart(self):
        self.playing_state = GamePlayState()
        self.gameover_state = None
        self.listener(GameState.START)
