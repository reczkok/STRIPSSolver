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
goal = [[1], [2], [3, 4], []]
subgoal = [[1], [2], [4], [3]]
subgoal2 = [[1], [2], [3], [4]]
goal2 = [[], [1], [2, 4, 3], []]
subgoal2_1 = [[1], [2], [4, 3], []]
subgoal2_2 = [[1], [], [2, 4, 3], []]
goal3 = [[1], [2], [4], [3]]
subgoal3_1 = [[1], [2, 3], [], [4]]
subgoal3_2 = [[1], [2, 3], [4], []]
# Subgoals are declared using a list of lists of lists eg: [[[1], [2], [4, 3], []]] - there can be multiple subgoals
subgoals = [
    [[1], [2], [4, 3], []]
]
# You can declare your own heuristic function (look at bots.heuristic to see how it is done),
# default is a function that returns 0

# bots.solve(goal=[[1], [], [3,4,2], []], heuristic=bots.heuristic)
# bots.solve(goal=[[1], [], [3,4,2], []])
# print("================ VANILLA SOLUTION 1 ===================")
# bots.solve(goal=goal, in_order=True)
# print("================ VANILLA SOLUTION 2 ===================")
# bots.solve(goal=goal2, in_order=False)
# print("================ VANILLA SOLUTION 3 ===================")
# bots.solve(goal=goal3)


# print("=============== HEURISTIC SOLUTION 1 ==================")
# bots.solve(goal=goal, heuristic=bots.heuristic)
# print("=============== HEURISTIC SOLUTION 2 ==================")
# bots.solve(goal=goal2, heuristic=bots.heuristic)
# print("=============== HEURISTIC SOLUTION 3 ==================")
# bots.solve(goal=goal3, heuristic=bots.heuristic)

#
# print("=============== SUBGOAL SOLUTION 1 ==================")
# bots.solve(goal=goal, subgoals=[subgoal, subgoal2], heuristic=bots.heuristic, in_order=False)
# print("=============== SUBGOAL SOLUTION 2 ==================")
# bots.solve(goal=goal, subgoals=[subgoal2_1, subgoal2_2], heuristic=bots.heuristic, in_order=False)
# print("=============== SUBGOAL SOLUTION 2 w/o h ==================")
# bots.solve(goal=goal, subgoals=[subgoal2_1, subgoal2_2], in_order=False)
# print("=============== SUBGOAL SOLUTION 3 ==================")
# bots.solve(goal=goal, subgoals=[subgoal3_1, subgoal3_2], in_order=False, heuristic=bots.heuristic)

# goal4 = [[4], [3], [2], [1]]
# subgoal4_1 = [[1], [2], [3, 4], []]
# subgoal4_2 = [[], [2], [4, 3], [1]]
#
# print("=============== HEURISTIC SOLUTION 4 ==================")
# bots.solve(goal=goal4, heuristic=bots.heuristic, subgoals=[subgoal4_1, subgoal4_2], in_order=False)

goal5 = [[1], [2], [3], [4]]
subgoal5_1 = [[1], [3], [2], [4]]
subgoal5_2 = [[4], [2], [3], [1]]
print("=============== HEURISTIC SOLUTION 5 ==================")
bots.solve(goal=goal5, heuristic=bots.heuristic, subgoals=[subgoal5_1, subgoal5_2], in_order=False)
