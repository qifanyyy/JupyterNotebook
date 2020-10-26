from Problems import Problem_Class1


class Uniform_Cost:
    visited_states = []
    ordered_state_array = []
    queue = []
    stop = False
    cntr = 200
    def __init__(self):
        a = 2
        for i in range(200):
            self.ordered_state_array.append(i)

    def solve(self, problem_instance):

        print("\nUniform_Cost:")
        self.queue = []
        self.visited_states = []
        self.stop = False
        self.queue.append([problem_instance.initial_state(), ''])
        current_state = None

        numberOfProduced = 0
        numberOfExpanded = 0
        depth = 0
        maxNumberOfNodesInMem = 0

        while not self.stop:
            mx = len(self.visited_states) + len(self.queue)
            if mx > maxNumberOfNodesInMem:
                maxNumberOfNodesInMem = mx
            self.cntr = self.cntr - 1
            if len(self.queue) == 0:
                print("no solution found!!")
                break
            current_state = self.queue.pop(0)
            # print(current_state)

            temp_state = current_state
            if not problem_instance.goal_state(current_state[0]):
                tmp_childs = problem_instance.get_childs(current_state[0])
                numberOfProduced += len(tmp_childs)
                numberOfExpanded += 1
                for child_state in tmp_childs:
                    if not self.repetitive_state(child_state[0], problem_instance):
                        self.visited_states.append(child_state[0])
                        if temp_state == None:
                            self.queue.append([child_state[0], child_state[1]])
                        else:
                            self.queue.append([child_state[0], temp_state[1] + ' ' + child_state[1]])
            else:
                self.stop = True
                print("moves:" + current_state[1])
                print("depth: " + str(current_state[1].count(' ')))
                print("number of expanded: " + str(numberOfExpanded))
                print("number of produced: " + str(numberOfProduced))
                print("max number of nodes in memory: " + str(maxNumberOfNodesInMem))

    def repetitive_state(self, state, problem_instance: Problem_Class1.Problem_Class1):
        for s in self.visited_states:
            if problem_instance.check_state_equality(s, state):
                return True
        return False


