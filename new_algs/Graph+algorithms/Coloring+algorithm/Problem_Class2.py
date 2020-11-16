import copy, random

class Problem_Class2:




    def __init__(self, logger):
        self.logger = logger


    def initial_state(self):
        # a = [2, 0, 6, 7, 3, 5, 1, 4, 8]
        a = [2,3,0,1,4,6,7,5,8]
        inversion_num = 2
        while inversion_num % 2 != 0:
            random.shuffle(a)
            index = 0
            inversion_num = 0
            for i in a:
                for j in range(8 - index):
                    if i > a[8 - j] and a[8 - j] != 0 and i != 0:
                        inversion_num = inversion_num + 1
                        # print(str(i) + " " + str(a[8 - j]))
                index = index + 1

            # print("inversion " + str(inversion_num))
        return a


    def final_state(self):
        return [1, 2, 3, 4, 5, 6, 7, 8, 0]


    def get_childs(self, state):
        child_states = []
        zero_index = 0
        for i in state:
            if i == 0:
                break
            zero_index = zero_index + 1

        if zero_index - 3 > -1:
            temp = []
            for n in state:
                temp.append(n)
            temp[zero_index] = temp[zero_index - 3]
            temp[zero_index - 3] = 0
            child_states.append([temp, 'U'])

        if zero_index + 3 < 9:
            temp = []
            for n in state:
                temp.append(n)
            temp[zero_index] = temp[zero_index + 3]
            temp[zero_index + 3] = 0
            child_states.append([temp, 'D'])


        if zero_index != 0 and zero_index != 3 and zero_index != 6:
            temp = []
            for n in state:
                temp.append(n)
            temp[zero_index] = temp[zero_index - 1]
            temp[zero_index - 1] = 0
            child_states.append([temp, 'L'])


        if zero_index != 2 and zero_index != 5 and zero_index != 8:
            temp = []
            for n in state:
                temp.append(n)
            temp[zero_index] = temp[zero_index + 1]
            temp[zero_index + 1] = 0
            child_states.append([temp, 'R'])


        return child_states


    def goal_state(self, state):
        # print(state)
        j = 1
        for i in state:
            if j == 9:
                j = 0
            if i != j:
                return False
            j = j + 1
        return True


    def check_state_equality(self, state1, state2):
        index = 0
        for i in state1:
            if state2[index] != i:
                # print(str(state2[index]) + " " + str(i))
                return False
            index = index + 1

        # print(str(state1) + " " + str(state2))

        return True

    def heuristic(self, state):
        distance = 0
        i = -1
        j = 0
        for n in state:

            i = i + 1
            if i > 2:
                j = j + 1
                i = 0

            if n == 0:
                distance = distance + 2 - i + 2 - j
            elif n == 1:
                distance = distance + i + j
            elif n == 2:
                distance = distance + abs(i - 1) + j
            elif n == 3:
                distance = distance + abs(i - 2) + abs(j)
            elif n == 4:
                distance = distance + abs(i) + abs(j - 1)
            elif n == 5:
                distance = distance + abs(i - 1) + abs(j - 1)
            elif n == 6:
                distance = distance + abs(i - 2) + abs(j - 1)
            elif n == 7:
                distance = distance + abs(i) + abs(j - 2)
            elif n == 8:
                distance = distance + abs(i - 1) + abs(j - 2)

        return distance