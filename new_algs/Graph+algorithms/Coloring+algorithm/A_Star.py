import operator

from Problems import Problem_Class1


class A_Star:
    visited_states = []
    queue = []
    stop = False
    move_cntr = 0
    def __init__(self):
        a = 2

    def solve(self, problem_instance):

        print("\nAstar:")
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
            self.move_cntr = self.move_cntr + 1

            mx = len(self.visited_states) + len(self.queue)
            if mx > maxNumberOfNodesInMem:
                maxNumberOfNodesInMem = mx

            cost_map = {}
            for s in self.queue:
                cost_map[self.queue.index(s)] = problem_instance.heuristic(s[0]) + s[1].count(' ')
            current_state = self.queue[sorted(cost_map.items(), key=operator.itemgetter(1), reverse=False)[0][0]]
            self.queue.remove(self.queue[sorted(cost_map.items(), key=operator.itemgetter(1), reverse=False)[0][0]])
            # print(current_state)

            numberOfExpanded += 1

            if not problem_instance.goal_state(current_state[0]):
                tmp_childs = problem_instance.get_childs(current_state[0])
                numberOfProduced += len(tmp_childs)
                for child_state in tmp_childs:
                    if not self.repetitive_state(child_state[0], problem_instance):
                        self.visited_states.append(child_state[0])
                        if current_state == None:
                            self.queue.append([child_state[0], child_state[1]])
                        else:
                            self.queue.append([child_state[0], current_state[1] + ' ' + child_state[1]])
            else:
                self.stop = True
                final = str(current_state[1])
                print("moves:" + final)
                print("depth: " + str(final.count(' ')))
                print("number of expanded: " + str(numberOfExpanded))
                print("number of produced: " + str(numberOfProduced))
                print("max number of nodes in memory: " + str(maxNumberOfNodesInMem))

    def repetitive_state(self, state, problem_instance: Problem_Class1.Problem_Class1):
        for s in self.visited_states:
            if problem_instance.check_state_equality(s, state):
                return True
        return False



