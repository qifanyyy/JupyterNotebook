import copy, random

class Problem_Class5:

    initial_green_number = 0
    def __init__(self, logger):
        self.logger = logger


    def initial_state(self):
        a = []

        for i in range(6):
            a.append([i+1, i+1, i+1, i+1, i+1, i+1, i+1, i+1, i+1])

        a = [[3,5,2,6,2,3,2,4,4],[1,1,5,5,5,2,3,1,3],[3,3,5,3,3,3,4,2,5],[6,5,1,1,1,6,6,5,6],[5,1,2,4,4,4,2,6,1],[1,2,4,2,6,4,4,6,6]]

        print("initial list: " + str(a) + " value: " + str(self.fitness(a)))
        return [a, ""]


    def get_random_neighbor(self, state):
        side = random.randrange(0, 6, 1)
        clockwise = random.randrange(0, 2, 1)
        if side == 0:
            #clockwise
            if clockwise == 1:
                temp_state = copy.deepcopy(state)
                tmp_val = temp_state[side][0]
                temp_state[side][0] = temp_state[side][6]
                temp_state[side][6] = temp_state[side][8]
                temp_state[side][8] = temp_state[side][2]
                temp_state[side][2] = tmp_val
                tmp_val = temp_state[side][1]
                temp_state[side][1] = temp_state[side][3]
                temp_state[side][3] = temp_state[side][7]
                temp_state[side][7] = temp_state[side][5]
                temp_state[side][5] = tmp_val

                tmp_arr = temp_state[1][0:3]
                temp_state[1][0:3] = temp_state[2][0:3]
                temp_state[2][0:3] = temp_state[3][0:3]
                al = temp_state[5][6:9]
                al.reverse()
                temp_state[3][0:3] = al
                tmp_arr.reverse()
                temp_state[5][6:9] = tmp_arr
                return [temp_state, "1C"]
            else:
                #anticlockwise
                temp_state = copy.deepcopy(state)
                tmp_val = temp_state[side][0]
                temp_state[side][0] = temp_state[side][2]
                temp_state[side][2] = temp_state[side][8]
                temp_state[side][8] = temp_state[side][6]
                temp_state[side][6] = tmp_val
                tmp_val = temp_state[side][1]
                temp_state[side][1] = temp_state[side][5]
                temp_state[side][5] = temp_state[side][7]
                temp_state[side][7] = temp_state[side][3]
                temp_state[side][3] = tmp_val

                tmp_arr = temp_state[1][0:3]
                al = temp_state[5][6:9]
                al.reverse()
                temp_state[1][0:3] = al
                al = temp_state[3][0:3]
                al.reverse()
                temp_state[5][6:9] = al
                temp_state[3][0:3] = temp_state[2][0:3]
                temp_state[2][0:3] = tmp_arr
                return [temp_state, "1A"]

        if side == 1:
            # clockwise
            if clockwise == 1:
                temp_state = copy.deepcopy(state)
                tmp_val = temp_state[side][0]
                temp_state[side][0] = temp_state[side][6]
                temp_state[side][6] = temp_state[side][8]
                temp_state[side][8] = temp_state[side][2]
                temp_state[side][2] = tmp_val
                tmp_val = temp_state[side][1]
                temp_state[side][1] = temp_state[side][3]
                temp_state[side][3] = temp_state[side][7]
                temp_state[side][7] = temp_state[side][5]
                temp_state[side][5] = tmp_val

                tmp_arr = copy.deepcopy(temp_state[0])
                temp_state[0][0] = temp_state[5][0]
                temp_state[0][3] = temp_state[5][3]
                temp_state[0][6] = temp_state[5][6]

                temp_state[5][0] = temp_state[4][0]
                temp_state[5][3] = temp_state[4][3]
                temp_state[5][6] = temp_state[4][6]

                temp_state[4][0] = temp_state[2][0]
                temp_state[4][3] = temp_state[2][3]
                temp_state[4][6] = temp_state[2][6]

                temp_state[2][0] = tmp_arr[0]
                temp_state[2][3] = tmp_arr[3]
                temp_state[2][6] = tmp_arr[6]
                return [temp_state, "2C"]

            else:
                # anticlockwise
                temp_state = copy.deepcopy(state)
                tmp_val = temp_state[side][0]
                temp_state[side][0] = temp_state[side][2]
                temp_state[side][2] = temp_state[side][8]
                temp_state[side][8] = temp_state[side][6]
                temp_state[side][6] = tmp_val
                tmp_val = temp_state[side][1]
                temp_state[side][1] = temp_state[side][5]
                temp_state[side][5] = temp_state[side][7]
                temp_state[side][7] = temp_state[side][3]
                temp_state[side][3] = tmp_val

                tmp_arr = copy.deepcopy(temp_state[0])
                temp_state[0][0] = temp_state[2][0]
                temp_state[0][3] = temp_state[2][3]
                temp_state[0][6] = temp_state[2][6]

                temp_state[2][0] = temp_state[4][0]
                temp_state[2][3] = temp_state[4][3]
                temp_state[2][6] = temp_state[4][6]

                temp_state[4][0] = temp_state[5][0]
                temp_state[4][3] = temp_state[5][3]
                temp_state[4][6] = temp_state[5][6]

                temp_state[5][0] = tmp_arr[0]
                temp_state[5][3] = tmp_arr[3]
                temp_state[5][6] = tmp_arr[6]
                return [temp_state, "2A"]


        if side == 2:
            # clockwise
            if clockwise == 1:
                temp_state = copy.deepcopy(state)
                tmp_val = temp_state[side][0]
                temp_state[side][0] = temp_state[side][6]
                temp_state[side][6] = temp_state[side][8]
                temp_state[side][8] = temp_state[side][2]
                temp_state[side][2] = tmp_val
                tmp_val = temp_state[side][1]
                temp_state[side][1] = temp_state[side][3]
                temp_state[side][3] = temp_state[side][7]
                temp_state[side][7] = temp_state[side][5]
                temp_state[side][5] = tmp_val

                tmp_arr = copy.deepcopy(temp_state[0])
                temp_state[0][6] = temp_state[1][8]
                temp_state[0][7] = temp_state[1][5]
                temp_state[0][8] = temp_state[1][2]

                temp_state[1][2] = temp_state[4][0]
                temp_state[1][5] = temp_state[4][1]
                temp_state[1][8] = temp_state[4][2]

                temp_state[4][0] = temp_state[3][6]
                temp_state[4][1] = temp_state[3][3]
                temp_state[4][2] = temp_state[3][0]

                temp_state[3][0] = tmp_arr[6]
                temp_state[3][3] = tmp_arr[7]
                temp_state[3][6] = tmp_arr[8]
                return [temp_state, "3C"]

            # anticlockwise
            else:
                temp_state = copy.deepcopy(state)
                tmp_val = temp_state[side][0]
                temp_state[side][0] = temp_state[side][2]
                temp_state[side][2] = temp_state[side][8]
                temp_state[side][8] = temp_state[side][6]
                temp_state[side][6] = tmp_val
                tmp_val = temp_state[side][1]
                temp_state[side][1] = temp_state[side][5]
                temp_state[side][5] = temp_state[side][7]
                temp_state[side][7] = temp_state[side][3]
                temp_state[side][3] = tmp_val

                tmp_arr = copy.deepcopy(temp_state[0])
                temp_state[0][6] = temp_state[3][0]
                temp_state[0][7] = temp_state[3][3]
                temp_state[0][8] = temp_state[3][6]

                temp_state[3][0] = temp_state[4][2]
                temp_state[3][3] = temp_state[4][1]
                temp_state[3][6] = temp_state[4][0]

                temp_state[4][0] = temp_state[1][2]
                temp_state[4][1] = temp_state[1][5]
                temp_state[4][2] = temp_state[1][8]

                temp_state[1][2] = tmp_arr[8]
                temp_state[1][5] = tmp_arr[7]
                temp_state[1][8] = tmp_arr[6]
                return [temp_state, "3A"]

        if side == 3:
            # clockwise
            if clockwise == 1:
                temp_state = copy.deepcopy(state)
                tmp_val = temp_state[side][0]
                temp_state[side][0] = temp_state[side][6]
                temp_state[side][6] = temp_state[side][8]
                temp_state[side][8] = temp_state[side][2]
                temp_state[side][2] = tmp_val
                tmp_val = temp_state[side][1]
                temp_state[side][1] = temp_state[side][3]
                temp_state[side][3] = temp_state[side][7]
                temp_state[side][7] = temp_state[side][5]
                temp_state[side][5] = tmp_val

                tmp_arr = copy.deepcopy(temp_state[0])
                temp_state[0][8] = temp_state[2][8]
                temp_state[0][5] = temp_state[2][5]
                temp_state[0][2] = temp_state[2][2]

                temp_state[2][2] = temp_state[4][2]
                temp_state[2][5] = temp_state[4][5]
                temp_state[2][8] = temp_state[4][8]

                temp_state[4][2] = temp_state[5][2]
                temp_state[4][5] = temp_state[5][5]
                temp_state[4][8] = temp_state[5][8]

                temp_state[5][2] = tmp_arr[2]
                temp_state[5][5] = tmp_arr[5]
                temp_state[5][8] = tmp_arr[8]
                return [temp_state, "4C"]

            # anticlockwise
            else:
                temp_state = copy.deepcopy(state)
                tmp_val = temp_state[side][0]
                temp_state[side][0] = temp_state[side][2]
                temp_state[side][2] = temp_state[side][8]
                temp_state[side][8] = temp_state[side][6]
                temp_state[side][6] = tmp_val
                tmp_val = temp_state[side][1]
                temp_state[side][1] = temp_state[side][5]
                temp_state[side][5] = temp_state[side][7]
                temp_state[side][7] = temp_state[side][3]
                temp_state[side][3] = tmp_val

                tmp_arr = copy.deepcopy(temp_state[0])
                temp_state[0][8] = temp_state[5][8]
                temp_state[0][5] = temp_state[5][5]
                temp_state[0][2] = temp_state[5][2]

                temp_state[5][2] = temp_state[4][2]
                temp_state[5][5] = temp_state[4][5]
                temp_state[5][8] = temp_state[4][8]

                temp_state[4][2] = temp_state[2][2]
                temp_state[4][5] = temp_state[2][5]
                temp_state[4][8] = temp_state[2][8]

                temp_state[2][2] = tmp_arr[2]
                temp_state[2][5] = tmp_arr[5]
                temp_state[2][8] = tmp_arr[8]
                return [temp_state, "4A"]


        if side == 4:
            # clockwise
            if clockwise == 1:
                temp_state = copy.deepcopy(state)
                tmp_val = temp_state[side][0]
                temp_state[side][0] = temp_state[side][6]
                temp_state[side][6] = temp_state[side][8]
                temp_state[side][8] = temp_state[side][2]
                temp_state[side][2] = tmp_val
                tmp_val = temp_state[side][1]
                temp_state[side][1] = temp_state[side][3]
                temp_state[side][3] = temp_state[side][7]
                temp_state[side][7] = temp_state[side][5]
                temp_state[side][5] = tmp_val

                tmp_arr = copy.deepcopy(temp_state[2])
                temp_state[2][6] = temp_state[1][6]
                temp_state[2][7] = temp_state[1][7]
                temp_state[2][8] = temp_state[1][8]

                temp_state[1][6] = temp_state[5][2]
                temp_state[1][7] = temp_state[5][1]
                temp_state[1][8] = temp_state[5][0]

                temp_state[5][0] = temp_state[3][8]
                temp_state[5][1] = temp_state[3][7]
                temp_state[5][2] = temp_state[3][6]

                temp_state[3][6] = tmp_arr[6]
                temp_state[3][7] = tmp_arr[7]
                temp_state[3][8] = tmp_arr[8]
                return [temp_state, "5C"]


            # anticlockwise
            else:
                temp_state = copy.deepcopy(state)
                tmp_val = temp_state[side][0]
                temp_state[side][0] = temp_state[side][2]
                temp_state[side][2] = temp_state[side][8]
                temp_state[side][8] = temp_state[side][6]
                temp_state[side][6] = tmp_val
                tmp_val = temp_state[side][1]
                temp_state[side][1] = temp_state[side][5]
                temp_state[side][5] = temp_state[side][7]
                temp_state[side][7] = temp_state[side][3]
                temp_state[side][3] = tmp_val

                tmp_arr = copy.deepcopy(temp_state[2])
                temp_state[2][6] = temp_state[3][6]
                temp_state[2][7] = temp_state[3][7]
                temp_state[2][8] = temp_state[3][8]

                temp_state[3][6] = temp_state[5][2]
                temp_state[3][7] = temp_state[5][1]
                temp_state[3][8] = temp_state[5][0]

                temp_state[5][0] = temp_state[1][8]
                temp_state[5][1] = temp_state[1][7]
                temp_state[5][2] = temp_state[1][6]

                temp_state[1][6] = tmp_arr[6]
                temp_state[1][7] = tmp_arr[7]
                temp_state[1][8] = tmp_arr[8]
                return [temp_state, "5A"]

        if side == 5:
            # clockwise
            if clockwise == 1:
                temp_state = copy.deepcopy(state)
                tmp_val = temp_state[side][0]
                temp_state[side][0] = temp_state[side][6]
                temp_state[side][6] = temp_state[side][8]
                temp_state[side][8] = temp_state[side][2]
                temp_state[side][2] = tmp_val
                tmp_val = temp_state[side][1]
                temp_state[side][1] = temp_state[side][3]
                temp_state[side][3] = temp_state[side][7]
                temp_state[side][7] = temp_state[side][5]
                temp_state[side][5] = tmp_val

                tmp_arr = copy.deepcopy(temp_state[4])
                temp_state[4][6] = temp_state[1][0]
                temp_state[4][7] = temp_state[1][3]
                temp_state[4][8] = temp_state[1][6]

                temp_state[1][0] = temp_state[0][2]
                temp_state[1][3] = temp_state[0][1]
                temp_state[1][6] = temp_state[0][0]

                temp_state[0][0] = temp_state[3][2]
                temp_state[0][1] = temp_state[3][5]
                temp_state[0][2] = temp_state[3][8]

                temp_state[3][2] = tmp_arr[8]
                temp_state[3][5] = tmp_arr[7]
                temp_state[3][8] = tmp_arr[6]
                return [temp_state, "6C"]


            # anticlockwise
            else:
                temp_state = copy.deepcopy(state)
                tmp_val = temp_state[side][0]
                temp_state[side][0] = temp_state[side][2]
                temp_state[side][2] = temp_state[side][8]
                temp_state[side][8] = temp_state[side][6]
                temp_state[side][6] = tmp_val
                tmp_val = temp_state[side][1]
                temp_state[side][1] = temp_state[side][5]
                temp_state[side][5] = temp_state[side][7]
                temp_state[side][7] = temp_state[side][3]
                temp_state[side][3] = tmp_val

                tmp_arr = copy.deepcopy(temp_state[4])
                temp_state[4][6] = temp_state[3][8]
                temp_state[4][7] = temp_state[3][5]
                temp_state[4][8] = temp_state[3][2]

                temp_state[3][8] = temp_state[0][2]
                temp_state[3][5] = temp_state[0][1]
                temp_state[3][2] = temp_state[0][0]

                temp_state[0][0] = temp_state[1][6]
                temp_state[0][1] = temp_state[1][3]
                temp_state[0][2] = temp_state[1][0]

                temp_state[1][0] = tmp_arr[6]
                temp_state[1][3] = tmp_arr[7]
                temp_state[1][6] = tmp_arr[8]
                return [temp_state, "6A"]


    def fitness(self, state):
        wrong_ones = 0
        index = 0

        for side in state:
            index += 1
            for i in side:
                if i != index:
                    wrong_ones += 1

        return 6*9 - wrong_ones