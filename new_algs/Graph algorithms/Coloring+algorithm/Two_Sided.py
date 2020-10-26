from Problems import Problem_Class1


class Two_Sided:
    visited_states = []
    visited_states2 = []
    queue = []
    queue2 = []
    stop = False
    cntr = 200
    def __init__(self):
        a = 2

    def solve(self, problem_instance: Problem_Class1.Problem_Class1):

        self.visited_states = []
        self.visited_states2 = []
        self.queue = []
        self.queue2 = []
        self.stop = False

        print("\nTwo sided:")
        self.queue.append([problem_instance.initial_state(), ''])
        self.queue2.append([problem_instance.final_state(), ''])
        current_state = None
        current_state2 = None

        b = True

        numberOfProduced = 0
        numberOfExpanded = 0
        depth = 0
        maxNumberOfNodesInMem = 0

        while not self.stop:
            mx = len(self.visited_states) + len(self.queue) + len(self.visited_states2) + len(self.queue2)
            if mx > maxNumberOfNodesInMem:
                maxNumberOfNodesInMem = mx

            self.cntr = self.cntr - 1
            b = not b
            if b :
                current_state = self.queue.pop(0)
                numberOfExpanded += 1
                temp_state = current_state
                # if not problem_instance.goal_state(current_state[0]):
                #     for child_state in problem_instance.get_childs(current_state[0]):
                #         if not self.repetitive_state(child_state[0], problem_instance):
                #             self.visited_states.append(child_state[0])
                #             if temp_state == None:
                #                 self.queue.append([child_state[0], child_state[1]])
                #             else:
                #                 self.queue.append([child_state[0], temp_state[1] + child_state[1]])
                # else:
                #     self.stop = True
                #     print(current_state[1])

                tmp_childs = problem_instance.get_childs(current_state[0])
                numberOfProduced += len(tmp_childs)
                for child_state in tmp_childs:
                    if not self.repetitive_state(child_state[0], problem_instance, self.visited_states):
                        if temp_state == None:
                            self.visited_states.append([child_state[0], child_state[1]])
                            self.queue.append([child_state[0], child_state[1]])
                        else:
                            self.visited_states.append([child_state[0], temp_state[1] + child_state[1]])
                            self.queue.append([child_state[0], temp_state[1] + ' ' + child_state[1]])
            else:
                current_state2 = self.queue2.pop(0)
                numberOfExpanded += 1
                temp_state = current_state2
                # if not problem_instance.goal_state(current_state2[0]):
                #     for child_state in problem_instance.get_childs(current_state2[0]):
                #         if not self.repetitive_state(child_state[0], problem_instance):
                #             self.visited_states2.append(child_state[0])
                #             if temp_state == None:
                #                 self.queue.append([child_state[0], child_state[1]])
                #             else:
                #                 self.queue.append([child_state[0], temp_state[1] + child_state[1]])
                # else:
                #     self.stop = True
                #     print(current_state2[1])
                tmp_childs = problem_instance.get_childs(current_state2[0])
                numberOfProduced += len(tmp_childs)
                for child_state in tmp_childs:
                    if not self.repetitive_state(child_state[0], problem_instance, self.visited_states2):
                        if temp_state == None:
                            self.visited_states2.append([child_state[0], child_state[1]])
                            self.queue2.append([child_state[0], child_state[1]])
                        else:
                            self.visited_states2.append([child_state[0], temp_state[1] + child_state[1]])
                            self.queue2.append([child_state[0], temp_state[1] + ' ' + child_state[1]])

            stopit = False
            for s1 in self.queue:
                if stopit:
                    break
                for s2 in self.queue2:
                    if problem_instance.check_state_equality(s1[0], s2[0]):
                        self.stop = True
                        # print(s1)
                        # print(s2)
                        main_str = ''
                        tmp_str = ''
                        for i in range(len(s2[1])):
                            tmp = s2[1][len(s2[1]) - i - 1]
                            # print(s2[1][i])
                            if tmp == 'R':
                                tmp_str2 = ''
                                for i in range(len(tmp_str)):
                                    tmp2 = tmp_str[len(tmp_str) - i - 1]
                                    tmp_str2 = tmp_str2 + tmp2
                                # print(tmp_str2)
                                main_str = main_str + tmp_str2
                                tmp_str = 'L'
                            elif tmp == 'L':
                                tmp_str2 = ''
                                for i in range(len(tmp_str)):
                                    tmp2 = tmp_str[len(tmp_str) - i - 1]
                                    tmp_str2 = tmp_str2 + tmp2
                                # print(tmp_str2)
                                main_str = main_str + tmp_str2
                                tmp_str = 'R'
                            else:
                                tmp_str = tmp_str + tmp
                        tmp_str2 = ''
                        for i in range(len(tmp_str)):
                            tmp2 = tmp_str[len(tmp_str) - i - 1]
                            tmp_str2 = tmp_str2 + tmp2
                        # print(tmp_str2)
                        main_str = main_str + tmp_str2
                        final = s1[1] + main_str
                        print("moves:" + final)
                        print("depth: " + str(final.count(' ')))
                        print("number of expanded: " + str(numberOfExpanded))
                        print("number of produced: " + str(numberOfProduced))
                        print("max number of nodes in memory: " + str(maxNumberOfNodesInMem))

                        stopit = True
                        break


    def repetitive_state(self, state, problem_instance: Problem_Class1.Problem_Class1, visited_states):
        for s in visited_states:
            if problem_instance.check_state_equality(s[0], state):
                return True
        return False




