import numpy as np

class Q_learning:

    def __init__(self, num_states, num_actions):
        self.EPSILON = 1
        self.EPSILON_DECAY = 0.99
        self.num_states = num_states
        self.num_actions = num_actions
        self.Q = np.zeros(shape=(num_states, num_actions))

        self.alpha = 1
        self.gamma = 0.998

    def update_policy(self, state,new_state, action, reward):
        self.Q[state, action] = self.Q[state,action]  + self.alpha*( reward + self.gamma*np.max(self.Q[new_state])  -\
                                                                     self.Q[state,action])

    def act(self, state):
        if np.random.rand() <  self.EPSILON :
            return np.random.randint(0, self.num_actions)
        return np.argmax(self.Q[state])

    def decay_epsilon(self):
        self.EPSILON *= self.EPSILON_DECAY