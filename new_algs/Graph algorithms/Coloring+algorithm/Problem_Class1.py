import copy

class Problem_Class1:




    def __init__(self, logger):
        self.logger = logger

    def initial_state(self):
        return [[True, 11, 12, 21, 22, 31, 32, 41, 42], [False]]

    def final_state(self):
        return [[False], [True, 11, 12, 21, 22, 31, 32, 41, 42]]

    def get_childs(self, state):
        child_states = []
        initial_boat_position = state[0][0]
        # state[0][0] = not state[0][0]
        # state[1][0] = not state[1][0]
        boat_moved = False
        if initial_boat_position:
            for p in state[0][1:]:
                boat_moved = True
                temp_state = copy.deepcopy(state)
                temp_state[0][0] = not state[0][0]
                temp_state[1][0] = not state[1][0]
                temp_state[0].remove(p)
                temp_state[1].append(p)
                child_states.append([temp_state, str(p)+'R'])
                for q in temp_state[0][1:]:
                    repetitive = self.aya_contains(p, q, child_states, False)
                    if ((list(str(p))[0] == list(str(q))[0]) or \
                            (list(str(p))[0] != list(str(q))[0] and list(str(p))[1] == list(str(q))[1])) and not repetitive:
                        temp_state2 = copy.deepcopy(temp_state)
                        temp_state2[0].remove(q)
                        temp_state2[1].append(q)
                        child_states.append([temp_state2, str(p)+str(q)+'R'])
        else:
            for p in state[1][1:]:
                boat_moved = True
                temp_state = copy.deepcopy(state)

                temp_state[0][0] = not state[0][0]
                temp_state[1][0] = not state[1][0]
                temp_state[1].remove(p)
                temp_state[0].append(p)
                child_states.append([temp_state, str(p)+'L'])
                for q in temp_state[1][1:]:
                    repetitive = self.aya_contains(p, q, child_states, True)
                    if ((list(str(p))[0] == list(str(q))[0]) or \
                            (list(str(p))[0] != list(str(q))[0] and list(str(p))[1] == list(str(q))[1])) and not repetitive:
                        temp_state2 = copy.deepcopy(temp_state)
                        temp_state2[1].remove(q)
                        temp_state2[0].append(q)
                        child_states.append([temp_state2, str(p)+str(q)+'L'])


        # state[0][0] = not state[0][0]
        # state[1][0] = not state[1][0]

        return child_states

    def aya_contains(self, o1, o2, array, look_left_side):
        b1 = False
        b2 = False
        b3 = False

        if look_left_side:
            for i in array:
                for j in i[0][1:]:
                    if j == o1:
                        b1 = True
                    if j == o2:
                        b2 = True
                if b1 and b2:
                    b3 = True
                b1 = False
                b2 = False
        else:
            for i in array:
                for j in i[1][1:]:
                    if j == o1:
                        b1 = True
                    if j == o2:
                        b2 = True
                if b1 and b2:
                    b3 = True
                b1 = False
                b2 = False

        # if b3:
        #     self.test(o1, o2, array, look_left_side)

        return b3

    # def test(self, o1, o2, array, look_left_side):
    #     b1 = False
    #     b2 = False
    #     print("---------------------------------")
    #     print(str(o1) + " " + str(o2) + "\n")
    #
    #     if look_left_side:
    #         for i in array:
    #             # print("\n")
    #
    #             for j in i[0][1:]:
    #                 # print("###" + str(j))
    #                 if j == o1:
    #                     b1 = True
    #                 if j == o2:
    #                     b2 = True
    #     else:
    #         for i in array:
    #             print("\n")
    #
    #             for j in i[1][1:]:
    #                 print("###" + str(j))
    #
    #                 if j == o1:
    #                     b1 = True
    #                 if j == o2:
    #                     b2 = True
    #
    #     return b1 and b2

    def goal_state(self, state):
        if len(state[0][1:]) == 0:
            return True
        return False

    def check_state_equality(self, state1, state2):
        for i in state1[0]:

            # print(str(i) + " " + str(state2))
            if not i in state2[0]:
                return False
            # else:
            #     print(str(i) + " " + str(state2))

        for i in state1[1]:
            # print(str(i) + " " + str(state2))
            if not i in state2[1]:
                return False
            # else:
            #     print(str(i) + " " + str(state2))

        # print(state1)
        # print(state2)
        # print("888888888888888888")

        return True