import copy, random

class Problem_Class3:

    initial_green_number = 0
    def __init__(self, logger):
        self.logger = logger


    def initial_state(self):
        a = [[1, 0, 0, 0, 0, 0, 0, 0], [0, 0, -1, 0, 0, 0, 0, 0], [0, 0, 0, 0, -1, 0, 0, 0], [0, 0, 0, 0, 0, 0, 2, 0],
             [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]]

        self.initial_green_number = 0
        for row in a:
            for i in row:
                if i == 2:
                    self.initial_green_number = self.initial_green_number + 1

        return a


    def get_childs(self, state):
        child_states = []
        i = -1
        j = 0
        found = False
        for row in state:
            if found:
                break
            for n in row:
                i = i + 1
                if i == 8:
                    i = 0
                    j = j + 1
                if n == 1:
                    found = True
                    break

        if j - 2 >= 0:
            #move code: 8
            if i - 1 >= 0 and state[j - 2][i - 1] != -1:
                tmp_state = copy.deepcopy(state)
                tmp_state[j][i] = 0
                tmp_state[j-2][i-1] = 1
                child_states.append([tmp_state, '8'])
            #move code: 1
            if i + 1 <= 7 and state[j - 2][i + 1] != -1:
                tmp_state = copy.deepcopy(state)
                tmp_state[j][i] = 0
                tmp_state[j-2][i+1] = 1
                child_states.append([tmp_state, '1'])
        if i + 2 <= 7:
            #move code: 2
            if j - 1 >= 0 and state[j - 1][i + 2] != -1:
                tmp_state = copy.deepcopy(state)
                tmp_state[j][i] = 0
                tmp_state[j-1][i+2] = 1
                child_states.append([tmp_state, '2'])
            #move code: 3
            if j + 1 <= 7 and state[j + 1][i + 2] != -1:
                tmp_state = copy.deepcopy(state)
                tmp_state[j][i] = 0
                tmp_state[j+1][i+2] = 1
                child_states.append([tmp_state, '3'])
        if j + 2 <= 7:
            # move code: 4
            if i + 1 <= 7 and state[j + 2][i + 1] != -1:
                tmp_state = copy.deepcopy(state)
                tmp_state[j][i] = 0
                tmp_state[j+2][i+1] = 1
                child_states.append([tmp_state, '4'])
            #move code: 5
            if i - 1 >= 0 and state[j + 2][i - 1] != -1:
                tmp_state = copy.deepcopy(state)
                tmp_state[j][i] = 0
                tmp_state[j+2][i-1] = 1
                child_states.append([tmp_state, '5'])
        if i - 2 >= 0:
            #move code: 6
            if j + 1 <= 7 and state[j + 1][i - 2] != -1:
                tmp_state = copy.deepcopy(state)
                tmp_state[j][i] = 0
                tmp_state[j+1][i-2] = 1
                child_states.append([tmp_state, '6'])
            #move code: 7
            if j - 1 >= 0 and state[j - 1][i - 2] != -1:
                tmp_state = copy.deepcopy(state)
                tmp_state[j][i] = 0
                tmp_state[j-1][i-2] = 1
                child_states.append([tmp_state, '7'])

        return child_states


    def goal_state(self, state):
        green_number = 0
        for row in state:
            for n in row:
                if n == 2:
                    green_number = green_number + 1

        return green_number != self.initial_green_number


    def check_state_equality(self, state1, state2):
        i = -1
        j = 0
        for row in state1:
            for n in row:
                i = i + 1
                if i == 8:
                    i = 0
                    j = j + 1

                if state2[j][i] != n:
                    return False

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