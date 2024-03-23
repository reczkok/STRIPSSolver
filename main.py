from RubiksCube1D import RubiksCube1D
from DockBots import DockBots

# cube = RubiksCube1D()
# cube.solve([6, 5, 4, 3, 2, 1])
# cube.solve([6, 5, 4, 3, 2, 1], cube.heuristic)

bots = DockBots()
# The piles are declared using a list of lists eg: [[1], [], [2, 4, 3], []] - there are exactly 4 piles and 4 containers
# The first element of a pile is the top of the pile
# You can declare where the robots start using a list eg: [1, 2, -1, -1] - there are exactly 2 robots
# You can also declare the initial state of the crates the same way as the piles
# the default is [[1], [2], [3], [4]]
goal = [[1], [], [2, 4, 3], []]
# Subgoals are declared using a list of lists of lists eg: [[[1], [2], [4, 3], []]] - there can be multiple subgoals
subgoals = [
    [[1], [2], [4, 3], []]
]
# You can declare your own heuristic function (look at bots.heuristic to see how it is done),
# default is a function that returns 0

# bots.solve(goal=[[1], [], [3,4,2], []], heuristic=bots.heuristic)
# bots.solve(goal=[[1], [], [3,4,2], []])
bots.solve(goal=goal, heuristic=bots.heuristic, subgoals=subgoals, in_order=True)
print("=============================================")
bots.solve(goal=goal, subgoals=subgoals)
