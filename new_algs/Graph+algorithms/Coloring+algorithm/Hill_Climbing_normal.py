import operator

from Problems import Problem_Class1


class Hill_Climbing_normal:
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

        print("\nHill_Climbing_normal:")
        self.queue = []
        self.visited_states = []
        self.queue.append([initial_state, ''])
        self.visited_states.append(self.queue[0][0])

        while not self.stop:
            self.move_cntr = self.move_cntr + 1

            cost_map = {}
            for s in self.queue:
                cost_map[self.queue.index(s)] = problem_instance.cost(s[0])
                # print(str(s) + " c: " + str(problem_instance.cost(s[0])))

            best = sorted(cost_map.items(), key=operator.itemgetter(1), reverse=False)[0]
            # print("best: " + str(best))
            if best[1] <= self.global_best:
                self.global_best = best[1]
                current_state = self.queue[best[0]]
                # print("current state: " + str(current_state))
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



