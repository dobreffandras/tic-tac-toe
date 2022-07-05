# tic-tac-toe

A tic-tac-toe implementation in Python using tkinter. 

## Goal

This repository is made just for training purposes. The goal is to have a tic-tac-toe game with a GUI where the user can play the game against the computer.

## Computer opponent

The computer opponent can work in two modes:
### Basic mode
This is the default functioning. The Computer opponent just fills up the board sequentially. 
### Strategic mode
In order to turn on strategic mode the following command must be run: `python .\strategy.py`
The command generates a `computer.strategy` file which contains the strategy model of the computer opponent.
The AI is based on the fact that [there's a best strategy for playing tic-tac-toe](https://cs.stanford.edu/people/eroberts/courses/soco/projects/1998-99/game-theory/zero.html). 
The difficulty determines how likely the computer will choose the best path in the games state-graph.

## Technology

The game is implemented in Python 3 using the built-in GUI framework [TkInter](https://wiki.python.org/moin/TkInter).

## Architecture and implementation

The classes representing the basic architecture of the implementation can be seen on the following diagram: 
```commandline
                                                                              ┌───────────────────┐
                                                                              │                   │
                                                                              │                   │
                                                                              │  Strategy         │
                                                                              │                   │
                                                                              │                   │
                                                                              └───────────────────┘
                                                                                      ▲
                                                                                      │
                                                                                      │
             ┌────────────────┐                     ┌───────────────────┐    ┌────────┴─────────┐
             │                │                     │                   │    │                  │
             │                │                     │                   │    │                  │
    ┌────────┤      Game      │◄───────────────────►│     GameEngine    ├───►│  ComputerPlayer  │
    │        │                │                     │                   │    │                  │
    │        │                │           ┌────────►│                   │    │                  │
    │        └────────────────┘           │         └─────────┬─────────┘    └──────────────────┘
    │                                     │                   │
    │                                     │                   │
    │                                     │                   │
    │        ┌────────────────┐           │                   ▼
    │        │                │           │         ┌───────────────────┐
    │        │                │           │         │                   │
    ├───────►│    Playing     ├───────────┤         │                   │
    │        │                │           │         │   GamePlayState   │
    │        │                │           │         │                   │
    │        └────────────────┘           │         │                   │
    │                                     │         └─────────┬─────────┘
    │        ┌────────────────┐           │                   │
    │        │                │           │                   │
    │        │                │           │                   ▼
    ├───────►│     Start      ├───────────┤         ┌───────────────────┐
    │        │                │           │         │                   │
    │        │                │           │         │                   │
    │        └────────────────┘           │         │     GameBoard     │
    │                                     │         │                   │
    │        ┌────────────────┐           │         │                   │
    │        │                │           │         └───────────────────┘
    │        │                │           │
    └───────►│    GameOver    ├───────────┘
             │                │
             │                │
             └────────────────┘

```

The main class is the `Game` which is just a scaffold for the three different stages of the game (Start, Playing, GameOver).
The `Game` class is a subclass of the `Tk` Tkinter class enabling the usage of the Tkinter.
All three classes that represent the stages of the game are nested classes of `Game`.
The `Start`, `Playing` and `GameOver` classes are only responsible for building up the UI, transferring the user interaction to the `GameEngine` and handling gamestate changes (by updating the UI).
All the three:
  - have a `setup_controls()` method that creates the UI elements and wires them up to the game engine
  - have a `layout_controls()` which does the layout of all

At the setup the `Game` instance registers its handler method to the `GameEngine`. The `Game` instance   
calls the `GameEngine` directly by its methods (like `launch()`, `start_playing()`).
The `GameEngine` notifies the `Game` about every state change using the registered 
handler. So the game can instantiate the appropriate class for the stage.
All three stages (`Start`, `Playing`, `GameOver`) behave similarly.

The `GameEngine` represents the stages of the game with a `GameState` enum.
The state of the game is represented by several attributes for the different stages (`playing_state`, `gameover_state`).
The `Playing` and `GameOver` classes are interested in these attributes.
The `playing_state` is more interesting. It holds a `GamePlayState` instance that represents the board (`GameBoard`)
and the player on turn (`GameTurn` enum).
Every time the `Playing` UI instance calls the `player_chooses()` method of the `GameEngine` the engine:
  - updates the state and notifies the UI about the change (on game over it changes the game stage)
  - switches the player to the computer player and notifies the UI about the change
  - requests the next move from the computer player
  - updates the state based on the move, switches the player to the user and notifies the UI about the change (on game over it changes the game stage)

The `GameEngine` uses a `ComputerPlayer` instance to drive the artificial opponent. 
But the `ComputerPlayer` class really just requests the next move from the `Strategy` instance based on the `GameBoard`.