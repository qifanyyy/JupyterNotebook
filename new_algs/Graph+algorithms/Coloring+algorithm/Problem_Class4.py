import copy, random

class Problem_Class4:

    initial_green_number = 0
    def __init__(self, logger):
        self.logger = logger


    def initial_state(self):
        a = []

        for i in range(12):
            a.append(random.randrange(0, 15, 1))

        print("initial list: " + str(a) + " cost: " + str(self.cost(a)))
        return a


    def get_childs(self, state):
        child_states = []
        index1 = -1
        index2 = 0
        for a in range(int(len(state))):
            index1 = index1 + 1
            if index1 == 3:
                index1 = 0
                index2 = index2 + 1

            for j in range(int(len(state)/3)):
                if j <= index2:
                    continue
                for i in range(3):
                    temp_state = copy.deepcopy(state)
                    tmp = temp_state[3*j + i]
                    temp_state[3*j + i] = temp_state[3*index2 + index1]
                    temp_state[3 * index2 + index1] = tmp
                    child_states.append([temp_state, ''])

        return child_states

    def get_first_better_child(self, state):
        index1 = -1
        index2 = 0
        numberOfProduced = 0
        cost = self.cost(state)
        for a in range(int(len(state))):
            index1 = index1 + 1
            if index1 == 3:
                index1 = 0
                index2 = index2 + 1

            for j in range(int(len(state)/3)):
                if j <= index2:
                    continue
                for i in range(3):
                    temp_state = copy.deepcopy(state)
                    tmp = temp_state[3*j + i]
                    temp_state[3*j + i] = temp_state[3*index2 + index1]
                    temp_state[3 * index2 + index1] = tmp
                    temp_cost = self.cost(temp_state)
                    numberOfProduced += 1
                    if temp_cost < cost:
                        print("val " + str(temp_cost))

                        return [temp_state, temp_cost, numberOfProduced]

        return None


    def check_state_equality(self, state1, state2):
        index = -1
        for a in state1:
            index = index + 1
            if a != state2[index]:
                return False

        return True


    def cost(self, state):
        cost = 0
        max = -1
        index = 0
        sum = 0
        for i in state:
            index = index + 1
            sum = sum + i
            if index % 3 == 0:
                if sum > max:
                    max = sum
                sum = 0

        return max