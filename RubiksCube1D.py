import time

from stripsProblem import STRIPS_domain, Strips, Planning_problem
from stripsForwardPlanner import Forward_STRIPS
from searchMPP import SearcherMPP


class RubiksCube1D:
    def __init__(self):
        self.boolean = {False, True}
        self.values = {1, 2, 3, 4, 5, 6}
        self.positions = {'pos1', 'pos2', 'pos3', 'pos4', 'pos5', 'pos6'}
        self.domain = STRIPS_domain(self.generate_domain_dict(), self.generate_actions())

    @staticmethod
    def heuristic(state, goal):
        return sum(abs(state[pos] - goal[pos]) for pos in state)

    def generate_domain_dict(self):
        domain_dict = {}
        for i in self.values:
            for j in self.positions:
                name = j + 'is' + str(i)
                domain_dict[name] = self.boolean
        return domain_dict

    def generate_actions(self):
        actions = []
        for i in range(1, 6):
            name = 'rotate' + str(i)
            for j in self.values:
                for k in self.values:
                    if j != k:
                        actions.append(Strips(name, {'pos' + str(i): j, 'pos' + str(i + 1): k},
                                              {'pos' + str(i): k, 'pos' + str(i + 1): j}))
        return actions

    def generate_problem(self, initial_state=[1, 2, 3, 4, 5, 6]):
        problem = Planning_problem(self.domain, self.generate_initial_state(initial_state), self.generate_goal())
        return problem

    def solve(self, initial_state=[1, 2, 3, 4, 5, 6], heuristic=None):
        problem = self.generate_problem(initial_state)
        if heuristic is None:
            planner = Forward_STRIPS(problem)
        else:
            planner = Forward_STRIPS(problem, heur=heuristic)
        searcher = SearcherMPP(planner)
        time1 = time.time()
        searcher.search()
        time2 = time.time()
        print('Time:', time2 - time1)

    @staticmethod
    def generate_initial_state(initial_state):
        state = {}
        for i in range(6):
            state['pos' + str(i + 1)] = initial_state[i]
        return state

    @staticmethod
    def generate_goal():
        goal = {}
        for i in range(6):
            goal['pos' + str(i + 1)] = i + 1
        return goal


