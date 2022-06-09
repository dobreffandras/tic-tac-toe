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