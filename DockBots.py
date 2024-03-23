import time

from stripsProblem import STRIPS_domain, Strips, Planning_problem
from stripsForwardPlanner import Forward_STRIPS
from searchMPP import SearcherMPP
from stripsRegressionPlanner import Regression_STRIPS, Subgoal
import re


class DockBots:
    def __init__(self):
        self.boolean = {False, True}
        self.locations = {'loc1', 'loc2', 'loc3', 'loc4'}
        self.robots = {'robot1', 'robot2'}
        self.cranes = {'crane1', 'crane2', 'crane3', 'crane4'}
        self.containers = {'container1', 'container2', 'container3', 'container4'}
        self.domain = STRIPS_domain(self.generate_domain_dict(), self.generate_actions())

    @staticmethod
    def heuristic(state, goal):
        goals = {x: goal[x] for x in goal if goal[x]}
        curr = {x: state[x] for x in state if state[x]}
        common_keys = set(goals.keys()).intersection(set(curr.keys()))
        return 100 - len(common_keys)

    def generate_domain_dict(self):
        domain_dict = {}
        for i in self.locations:
            for j in self.robots:
                name = j + 'at' + i
                domain_dict[name] = self.boolean
        for i in self.cranes:
            for j in self.locations:
                name = i + 'belong' + j
                domain_dict[name] = self.boolean
        for i in self.cranes:
            for j in self.containers:
                name = i + 'holding' + j
                domain_dict[name] = self.boolean
        for i in self.robots:
            name = i + 'unloaded'
            domain_dict[name] = self.boolean
        for i in self.robots:
            for j in self.containers:
                name = i + 'loaded' + j
                domain_dict[name] = self.boolean
        for i in self.cranes:
            name = i + 'empty'
            domain_dict[name] = self.boolean
        for i in self.cranes:
            for j in self.containers:
                name = i + 'holding' + j
                domain_dict[name] = self.boolean
        for i in self.locations:
            name = 'free' + i
            domain_dict[name] = self.boolean
        for i in self.containers:
            for j in self.locations:
                name = i + 'in' + j
                domain_dict[name] = self.boolean
        for i in self.containers:
            for j in self.locations:
                name = i + 'top' + j
                domain_dict[name] = self.boolean
        for i in self.containers:
            for j in self.containers:
                if i != j:
                    name = i + 'on' + j
                    domain_dict[name] = self.boolean
        return domain_dict

    def generate_actions(self):
        actions = []
        for i in self.locations:
            for j in self.locations:
                if i != j:
                    for k in self.robots:
                        name = 'move ' + k + ' from ' + i + ' to ' + j
                        actions.append(Strips(name, {k + 'at' + i: True, 'free' + j: True},
                                              {k + 'at' + j: True, 'free' + i: True, 'free' + j: False,
                                               k + 'at' + i: False}))
        for i in self.cranes:
            for j in self.locations:
                for k in self.containers:
                    for l in self.robots:
                        name = 'load ' + l + ' using ' + i + ' with ' + k + ' at ' + j
                        actions.append(Strips(name,
                                              {l + 'at' + j: True, i + 'belong' + j: True, i + 'holding' + k: True,
                                               l + 'unloaded': True},
                                              {l + 'loaded' + k: True, l + 'unloaded': False, i + 'empty': True,
                                               i + 'holding' + k: False}))
        for i in self.cranes:
            for j in self.locations:
                for k in self.containers:
                    for l in self.robots:
                        name = 'unload ' + l + ' using ' + i + ' with ' + k + ' at ' + j
                        actions.append(Strips(name, {i + 'belong' + j: True, l + 'at' + j: True, l + 'loaded' + k: True,
                                                     i + 'empty': True},
                                              {l + 'unloaded': True, i + 'holding' + k: True, l + 'loaded' + k: False,
                                               i + 'empty': False}))
        # first the situatuion where the container is the only one in the pile
        for i in self.cranes:
            for j in self.locations:
                for k in self.containers:
                    only_one_condition = {l + 'in' + j: False for l in self.containers if l != k}
                    name = 'take ' + k + ' from ' + j + ' using ' + i
                    actions.append(Strips(name, {i + 'belong' + j: True, i + 'empty': True, k + 'in' + j: True,
                                                 k + 'top' + j: True, **only_one_condition},
                                          {i + 'holding' + k: True, k + 'top' + j: False, k + 'in' + j: False,
                                           i + 'empty': False}))
        # now the situation where the container is not the only one in the pile
        for i in self.cranes:
            for j in self.locations:
                for k in self.containers:
                    for l in self.containers:
                        if k != l:
                            name = 'take ' + k + ' from ' + j + ' using ' + i
                            actions.append(Strips(name, {i + 'belong' + j: True, i + 'empty': True, k + 'in' + j: True,
                                                         k + 'top' + j: True, l + 'on' + k: True},
                                                  {i + 'holding' + k: True, k + 'top' + j: False, k + 'in' + j: False,
                                                   l + 'on' + k: False, i + 'empty': False}))
        for i in self.cranes:
            for j in self.locations:
                for k in self.containers:
                    for l in self.containers:
                        name = 'put ' + k + ' at ' + j + ' on ' + l + ' using ' + i
                        actions.append(
                            Strips(name, {i + 'belong' + j: True, i + 'holding' + k: True, l + 'top' + j: True},
                                   {k + 'on' + l: True, k + 'top' + j: True, k + 'in' + j: True, l + 'top' + j: False,
                                    i + 'holding' + k: False, i + 'empty': True}))
        # add case for situation when the container is getting placed on an empty pile
        for i in self.cranes:
            for j in self.locations:
                for k in self.containers:
                    empty_condition = {l + 'in' + j: False for l in self.containers if l != k}
                    name = 'put ' + k + ' at ' + j + ' on empty pile using ' + i
                    actions.append(Strips(name, {i + 'belong' + j: True, i + 'holding' + k: True, **empty_condition,
                                                 i + 'empty': True},
                                          {k + 'in' + j: True, k + 'top' + j: True, i + 'holding' + k: False,
                                           i + 'empty': True}))
        return actions

    def generate_problem(self, goal=[[1, 2, 3, 4], [], [], []], initial_state=[[1], [2], [3], [4]],
                         robots=[1, 2, -1, -1], in_order=False):
        problem = Planning_problem(self.domain, self.generate_initial_state(initial_state, robots),
                                   self.generate_goal(goal, in_order))
        return problem

    def solve(self, goal=[[1, 2, 3, 4], [], [], []], initial_state=[[1], [2], [3], [4]], robots=[1, 2, -1, -1],
              heuristic=None, subgoals=None, in_order=False):
        if subgoals is None:
            problem = self.generate_problem(goal, initial_state, robots, in_order)
            if heuristic is None:
                planner = Forward_STRIPS(problem)
            else:
                planner = Forward_STRIPS(problem, heur=heuristic)
            searcher = SearcherMPP(planner)
            time1 = time.time()
            searcher.search()
            time2 = time.time()
            print('Time:', time2 - time1)
            return searcher.solution.arc.from_node.assignment
        else:
            subgoals.append(goal)
            first_subgoal = True
            while len(subgoals) > 0:
                subgoal = subgoals.pop(0)
                if first_subgoal:
                    problem = Planning_problem(self.domain, self.generate_initial_state(initial_state, robots),
                                           self.generate_goal(subgoal, in_order))
                    first_subgoal = False
                else:
                    problem = Planning_problem(self.domain, initial_state, self.generate_goal(subgoal, in_order))
                if heuristic is None:
                    planner = Forward_STRIPS(problem)
                else:
                    planner = Forward_STRIPS(problem, heur=heuristic)
                searcher = SearcherMPP(planner)
                time1 = time.time()
                searcher.search()
                time2 = time.time()
                print('Time:', time2 - time1)
                initial_state = searcher.solution.arc.to_node.assignment
            return initial_state

    def generate_initial_state(self, initial_state, robots):
        state = {}
        robot1init = ''
        robot2init = ''
        for i, x in enumerate(robots):
            if x == 1:
                robot1init = 'loc' + str(i + 1)
            elif x == 2:
                robot2init = 'loc' + str(i + 1)

        container1init = ''
        container2init = ''
        container3init = ''
        container4init = ''
        add_info = []
        for i, x in enumerate(initial_state):
            if len(x) != 0:
                for cont in x:
                    if cont == 1:
                        container1init = 'loc' + str(i + 1)
                    elif cont == 2:
                        container2init = 'loc' + str(i + 1)
                    elif cont == 3:
                        container3init = 'loc' + str(i + 1)
                    elif cont == 4:
                        container4init = 'loc' + str(i + 1)
                if len(x) > 1:
                    for j in range(len(x) - 1):
                        add_info.append('container' + str(x[j]) + 'on' + 'container' + str(x[j + 1]))
                        if j + 1 == len(x) - 1:
                            add_info.append('container' + str(x[j + 1]) + 'top' + 'loc' + str(i + 1))
                else:
                    add_info.append('container' + str(x[0]) + 'top' + 'loc' + str(i + 1))

        for i in self.locations:
            for j in self.robots:
                state[j + 'at' + i] = False
        for i in self.robots:
            for j in self.containers:
                state[i + 'loaded' + j] = False
        for i in self.locations:
            state['free' + i] = True
        for i in self.cranes:
            for j in self.locations:
                state[i + 'belong' + j] = False
        for i in self.cranes:
            for j in self.containers:
                state[i + 'holding' + j] = False
        for i in self.robots:
            state[i + 'unloaded'] = True
        for i in self.cranes:
            state[i + 'empty'] = True
        for i in self.containers:
            for j in self.locations:
                state[i + 'in' + j] = False
        for i in self.containers:
            for j in self.containers:
                state[i + 'on' + j] = False
        for i in self.containers:
            for j in self.locations:
                if i != j:
                    state[i + 'top' + j] = False
        state['robot1at' + robot1init] = True
        state['robot2at' + robot2init] = True
        state['free' + robot1init] = False
        state['free' + robot2init] = False
        state['crane1belong' + 'loc1'] = True
        state['crane2belong' + 'loc2'] = True
        state['crane3belong' + 'loc3'] = True
        state['crane4belong' + 'loc4'] = True
        state['crane1empty'] = True
        state['crane2empty'] = True
        state['crane3empty'] = True
        state['crane4empty'] = True
        state['container1in' + container1init] = True
        state['container2in' + container2init] = True
        state['container3in' + container3init] = True
        state['container4in' + container4init] = True
        state['container1top' + container1init] = True
        state['container2top' + container2init] = True
        state['container3top' + container3init] = True
        state['container4top' + container4init] = True
        for i in add_info:
            state[i] = True
        return state

    @staticmethod
    def generate_goal(goal, in_order=False):
        # [[1, 2, 3, 4], [], [], []] represents the goal state
        # the first list represents the first pile and so on
        goal_state = {}
        for i in range(4):
            if len(goal[i]) == 0:
                continue
            for j in range(len(goal[i])):
                goal_state['container' + str(goal[i][j]) + 'in' + 'loc' + str(i + 1)] = True
            if in_order:
                goal_state['container' + str(goal[i][0]) + 'top' + 'loc' + str(i + 1)] = True
                if len(goal[i]) > 1:
                    for j in range(len(goal[i]) - 1):
                        goal_state['container' + str(goal[i][j]) + 'on' + 'container' + str(goal[i][j + 1])] = True
        return goal_state
