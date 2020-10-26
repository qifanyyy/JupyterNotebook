from Q_learning_Singleagent.GridWorld import Gridworld as Env
from Q_learning_Singleagent.QLearning import Q_learning as Q

import matplotlib.pyplot as plt

def play_game():

    rows = 10
    columns = 10
    num_states = rows * columns
    num_actions = 4
    target_pos = (rows-1, columns-1)

    env = Env(rows, columns ,num_states, num_actions, target_pos)

    agent = Q(rows * columns, num_actions)

    done = False
    EPISODES = 1000

    STEPS = []

    for episode in range(EPISODES):

        done = False
        env.reset()
        steps = 0
        state = env.get_discrete_state(env.position)

        while not done:
            steps += 1
            action = agent.act(state)
            new_state, reward, done = env.step(action)
            new_state = env.get_discrete_state(env.position)
            agent.update_policy(state,new_state, action, reward)
            state = new_state

        print (f"Episode {episode}  -- {steps} steps")
        agent.decay_epsilon()
        STEPS.append(steps)

    plt.plot(range(EPISODES),STEPS,legend="Q learning agent")
    plt.legend()
    plt.xlabel("Episodes")
    plt.ylabel("Steps")
    plt.show()

if __name__ == "__main__":
    play_game()


