from enum import Enum
from collections.abc import Callable


class GameState(Enum):
    START = "START"
    PLAYING = "PLAYING"
    GAMEOVER = "GAMEOVER"


class GameEngine:
    def __init__(self, gamestate_listener: Callable[[GameState], None]):
        self.listener = gamestate_listener

    def launch(self):
        self.listener(GameState.PLAYING)
