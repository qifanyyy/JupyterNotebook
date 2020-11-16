import numpy as np
from scipy.optimize import linprog

class MinimaxQ:

    def __init__(self, num_states ,num_actions_a, num_actions_b, gamma,alpha =  1, expl = 1):

        self.num_states = num_states
        self.num_actions_a = num_actions_a
        self.num_actions_b = num_actions_b

        self.gamma = gamma

        self.V = np.ones(num_states)
        self.pi = np.ones((num_states,num_actions_a)) / num_states
        self.Q = np.random.random((num_states, num_actions_a, num_actions_b))

        self.alpha = 1
        self.decay = 0.998
        self.learning = True

        self.expl = expl

    def choose_action(self, state):
        if np.random.rand() < self.expl:
            return np.random.randint(low=0, high=self.num_actions_a)

        return self.weightedActionChoice(state)



    def weightedActionChoice(self, state):

        rand = np.random.rand()
        cumSumProb = np.cumsum(self.pi[state])
        action = 0

        while rand > cumSumProb[action]:
            action += 1
        return action

    def getReward(self, initial_state, final_state, actions, reward, restrict_actions=None):

        if not self.learning:
            return None

        action_a, action_b = actions
        self.Q[initial_state, action_a, action_b] = self.Q[initial_state, action_a, action_b] + \
                                                   self.alpha * (reward + self.gamma * np.max(self.Q[final_state]) - self.Q[final_state])

        #self.V[initial_state] = self.update_policy(initial_state)
        self.V[initial_state] = min(np.sum(self.Q[initial_state].T) * self.pi[initial_state], axis=1)
        self.alpha *= self.decay

    def update_policy(self, state, retry=False):

        c = np.zeros(self.num_actions_a + 1)
        c[0] = -1
        A_ub = np.ones((self.num_actions_a, self.num_actions_b + 1))
        A_ub[:, 1:] = -self.Q[state].T
        b_ub = np.zeros(self.num_actions_a)
        A_eq = np.ones((1, self.num_actions_a + 1))
        A_eq[0, 0] = 0
        b_eq = [1]
        bounds = ((None, None),) + ((0, 1),) * self.num_actions_a

        res = linprog(c, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq, bounds=bounds)

        if res.success:
            self.pi[state] = res.x[1:]
        elif not retry:
            return self.update_policy(state, retry=True)
        else:
            print("Alert : %s" % res.message)
            return self.V[state]

        return res.x[0]

if __name__ == '__main__':

    def testUpdatePolicy():
        m = MinimaxQ(1, 2, 2, 1e-4, 0.2, 0.9)
        m.Q[0] = [[0, 1], [1, 0.5]]
        m.update_policy(0)
        print(m.pi)

    testUpdatePolicy()



