from enum import Enum
from collections.abc import Callable


class GameState(Enum):
    START = "START"
    PLAYING = "PLAYING"
    GAMEOVER = "GAMEOVER"


class GameEngine:
    def __init__(self, gamestate_listener: Callable[[GameState], None]):
        self.listener = gamestate_listener
        self.playing_state = []

    def launch(self):
        self.listener(GameState.START)

    def start_playing(self):
        self.listener(GameState.PLAYING)

    def player_chooses(self, r, c):
        print("Player Chooses", r, c)
        self.playing_state.append((r,c))
        self.playing_state_listener(self.playing_state)

    def connect_playing_state_change_handler(self, playing_state_listener : Callable[[object], None]):
        self.playing_state_listener = playing_state_listener
