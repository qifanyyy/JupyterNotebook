import numpy as np
import Q_learning_Singleagent as Q

class Gridworld:
    def __init__(self,rows, columns ,num_states, num_actions, target_pos):

        self.rows = rows
        self.columns = columns
        self.alpha = 0.95
        self.gamma = 0.99
        self.env = np.zeros(shape=(rows, columns))
        self.num_states = num_states
        self.num_actions = num_actions
        self.target_pos = target_pos
        self.position = (0,0)
        self.discrete_states = self.discretize_states()

    def reset(self):
        self.__init__(self.rows, self.columns ,self.num_states, self.num_actions, self.target_pos)

    def discretize_states(self):

        num_state = 0
        states = {}
        for i in range(self.rows):
            for j in range(self.columns):
                states[(i,j)] = num_state
                num_state += 1
        return states

    def get_discrete_state(self,position):
        num_state = 0
        for i in range(self.rows):
            for j in range(self.columns):
                if (i,j) == position:
                    return self.discrete_states[(i, j)]
                num_state += 1
        return None


    # 0 move left
    # 1 move right
    # 2 move down
    # 3 move up
    def valid_position(self, action):

        row , column = self.position

        if action == 0 and column - 1 >= 0:
            return True

        if action == 1 and column + 1 < self.columns:
            return True

        if action == 2 and row + 1 < self.rows:
            return True

        if action == 3 and row - 1 >= 0:
            return True

        return False

    # 0 move left
    # 1 move right
    # 2 move down
    # 3 move up
    # Returns None if the player didnt move ....
    def move(self, action):

        row, column = self.position

        if self.valid_position(action):

            if action == 0:
                column -= 1

            if action == 1:
                column += 1

            if action == 2:
                row += 1

            if action == 3:
                row -= 1

            self.position = (row, column)

            return self.position
        return None

    def step(self, action):

        old_position = self.position
        position = self.move(action)

        # the player didnt move
        if position == None:
            return self.get_discrete_state(old_position), - 10, False

        self.env[old_position] = 0
        self.env[position] = 1

        return self.get_discrete_state(position), 100 if position == self.target_pos else -1, True if self.target_pos == position else False




