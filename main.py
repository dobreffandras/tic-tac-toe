from game import Game
from strategy import ComputerStrategyBuilder, BasicStrategy
import strategy

# classes in saved computer.strategy file must be loaded into the __main__ namespace
# because deserialization only detects classes in the correct namespace
module_dict = globals()
module_dict["ComputerStrategy"] = strategy.ComputerStrategy
module_dict["StrategyNode"] = strategy.StrategyNode
module_dict["Winner"] = strategy.Winner

loaded_strategy = ComputerStrategyBuilder(strategy.FILENAME).load()
if loaded_strategy:
    print("Computer is playing with winning strategy.")
    Game(loaded_strategy).launch()
else:
    print("Computer is playing with basic strategy.")
    Game(BasicStrategy()).launch()
