import operator

from Problems import Problem_Class1


class Hill_Climbing_firstChoice:
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

        print("\nHill_Climbing_firstChoice:")
        self.queue = []
        self.visited_states = []
        current_state = [initial_state, '']

        while not self.stop:
            self.move_cntr = self.move_cntr + 1

            self.numberOfExpanded += 1
            temp = problem_instance.get_first_better_child(current_state[0])
            best = []
            best.append("")
            best.append("")

            # print("best: " + str(temp))
            if temp != None:
                best[0] = temp[0]
                best[1] = temp[1]
                self.numberOfProduced += temp[2]
                self.global_best = best[1]
                current_state = best
                # print("current state: " + str(current_state))
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



