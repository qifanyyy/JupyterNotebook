import sys

from Problems import Problem_Class1


class DFS_Iterative_Deepening:
    visited_states = []
    ordered_state_array = []
    test = []
    stop = False
    max_depth = 1
    initial_state = None
    cntr = 200
    numberOfProduced = 0
    numberOfExpanded = 0
    depth = 0
    maxNumberOfNodesInMem = 0
    numberOfVisited1 = -1
    numberOfVisited2 = 0
    def __init__(self):
        max_depth = 1
        sys.setrecursionlimit(10000)
        a = 2
        for i in range(10000):
            self.ordered_state_array.append(0)

    def solve(self, problem_instance, current_state, depth):
        # self.cntr = self.cntr - 1
        # if self.cntr < 0:
        #     self.stop = True
        # print(depth)

        if self.stop or depth >= self.max_depth:
            return

        current_state2 = None
        if current_state == None:
            current_state2 = problem_instance.initial_state()
            self.initial_state = current_state2
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
                        print("moves:" + finalString)
                        print("depth: " + str(depth+1))
                        print("number of expanded: " + str(self.numberOfExpanded))
                        print("number of produced: " + str(self.numberOfProduced))
                        print("max number of nodes in memory: " + str(self.maxNumberOfNodesInMem))
                        return
                    else:

                        self.solve(problem_instance, child_state[0], depth + 1)

        if depth == 0 and not self.stop:
            self.numberOfVisited2 = len(self.visited_states)
            if self.numberOfVisited1 == self.numberOfVisited2:
                self.stop = True
                print("no solution found!!")
                return
            self.numberOfVisited1 = self.numberOfVisited2
            self.visited_states = []
            self.ordered_state_array = []
            for i in range(40000):
                self.ordered_state_array.append(0)
            self.max_depth = self.max_depth + 1
            # print(self.max_depth)
            self.ordered_state_array[0] = " "
            self.visited_states.append(self.initial_state)
            self.solve(problem_instance, self.initial_state, 0)


    def repetitive_state(self, state, problem_instance: Problem_Class1.Problem_Class1):
        for s in self.visited_states:
            if problem_instance.check_state_equality(s, state):
                return True
        return False



