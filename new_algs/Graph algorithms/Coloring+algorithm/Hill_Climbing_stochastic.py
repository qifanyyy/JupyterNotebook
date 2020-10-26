import operator, random

from Problems import Problem_Class1


class Hill_Climbing_stochastic:
    visited_states = []
    ordered_state_array = []
    queue = []
    stop = False
    move_cntr = 0
    global_best = 9999
    numberOfProduced = 0
    numberOfExpanded = 0
    def __init__(self):
        a = 2

    def solve(self, problem_instance, initial_state):

        print("\nHill_Climbing_stochastic:")
        self.queue = []
        self.visited_states = []
        self.queue.append([initial_state, ''])
        self.visited_states.append(self.queue[0][0])

        while not self.stop:
            self.move_cntr = self.move_cntr + 1

            better_states = []
            cost_map = {}
            for s in self.queue:
                if problem_instance.cost(s[0]) <= self.global_best:
                    better_states.append(s)
            self.queue = better_states

            if len(self.queue) != 0:
                current_state = self.queue[random.randrange(0, len(self.queue), 1)]
                self.global_best = problem_instance.cost(current_state[0])
                self.queue = []
                self.numberOfExpanded += 1
                tmp_childs = problem_instance.get_childs(current_state[0])
                self.numberOfProduced += len(tmp_childs)
                for child_state in tmp_childs:
                    if not self.repetitive_state(child_state[0], problem_instance):
                        self.visited_states.append(child_state[0])
                        if current_state == None:
                            self.queue.append([child_state[0], child_state[1]])
                        else:
                            self.queue.append([child_state[0], current_state[1] + child_state[1]])
            else:
                self.stop = True
                print("solution: " + str(current_state[0]) + " cost: " + str(problem_instance.cost(current_state[0])))
                print("number of expanded: " + str(self.numberOfExpanded))
                print("number of produced: " + str(self.numberOfProduced))

    def repetitive_state(self, state, problem_instance: Problem_Class1.Problem_Class1):
        for s in self.visited_states:
            if problem_instance.check_state_equality(s, state):
                return True
        return False



