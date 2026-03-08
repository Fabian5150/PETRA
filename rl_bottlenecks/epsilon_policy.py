import numpy as np

"""
Decides the next action (either explorative or exploitative) based on the current state
and the current exploration rate epsilon
"""
def epsilon_greedy_action(q_table, state, epsilon, n_actions):
    if np.random.random() < epsilon:
        # exploration
        return np.random.randint(0, n_actions)
    else:
        # exploitation
        return np.argmax(q_table[state])

"""
Updates the exploration rate epsilon with exponential decay
based on the current episode
Starts exploratiev and becomes gradually more exploitative
"""
def update_epsilon(episode, epsilon_start=1.0, epsilon_min=0.01, epsilon_decay=0.001):
    epsilon = epsilon_start * np.exp(-epsilon_decay * episode)

    return max(epsilon_min, epsilon)