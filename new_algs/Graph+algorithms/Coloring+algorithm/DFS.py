import sys

from Problems import Problem_Class1


class DFS:
    visited_states = []
    ordered_state_array = []
    test = []
    stop = False
    cntr = 200
    numberOfProduced = 0
    numberOfExpanded = 0
    depth = 0
    maxNumberOfNodesInMem = 0

    def __init__(self):
        sys.setrecursionlimit(10000)
        a = 2
        for i in range(10000):
            self.ordered_state_array.append(0)

    def solve(self, problem_instance, current_state, depth):
        # print(len(self.ordered_state_array))
        # print(self.visited_states)
        # print("-----------------")
        if self.stop:
            return
        current_state2 = None
        if current_state == None:
            current_state2 = problem_instance.initial_state()
            self.visited_states = []
            self.ordered_state_array = []
            for i in range(10000):
                self.ordered_state_array.append(0)
            self.ordered_state_array[0] = " "
            self.visited_states.append(current_state2)
        else:
            current_state2 = current_state

        mx = len(self.visited_states) + depth
        if mx > self.maxNumberOfNodesInMem:
            self.maxNumberOfNodesInMem = mx

        if not problem_instance.goal_state(current_state2):
            # print("parent: " + str(current_state2))
            # for child_state in problem_instance.get_childs(current_state2):
            #     print("child: " + str(child_state))
            self.numberOfExpanded += 1
            tmp_childs = problem_instance.get_childs(current_state2)
            self.numberOfProduced += len(tmp_childs)
            for child_state in tmp_childs:
                if not self.repetitive_state(child_state[0], problem_instance):
                    # print(depth)
                    # print(child_state)
                    self.ordered_state_array[depth + 1] = child_state[1]
                    self.visited_states.append(child_state[0])

                    if problem_instance.goal_state(child_state[0]):
                        self.stop = True
                        finalString = " "
                        for s in self.ordered_state_array:
                            if s == 0:
                                break
                            finalString += str(s) + ' '
                        print("moves: " + finalString)
                        print("depth: " + str(depth+1))
                        print("number of expanded: " + str(self.numberOfExpanded))
                        print("number of produced: " + str(self.numberOfProduced))
                        print("max number of nodes in memory: " + str(self.maxNumberOfNodesInMem))
                        return
                    else:
                        self.solve(problem_instance, child_state[0], depth + 1)
                # else:
                #     print(child_state)


    def repetitive_state(self, state, problem_instance: Problem_Class1.Problem_Class1):
        for s in self.visited_states:
            if problem_instance.check_state_equality(s, state):
                return True
        return False



