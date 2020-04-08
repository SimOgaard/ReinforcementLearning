import numpy as np

class Agent1:
    
    def __init__(self, state_size, action_size):
        self.state_size = state_size
        self.action_size = action_size

        self.q_table = np.zeros([self.state_size, self.action_size])

        self.random_action = 0
        self.max_min_action = 0
        self.total_reward = 0

        self.gamma = 0.1
        self.alpha = 0.1
        self.epsilon = 1
        self.epsilon_decay = 0.8

    def act(self, state):
        if np.random.rand() < self.epsilon:
            self.random_action += 1
            return np.random.randint(self.action_size)
        else:
            self.max_min_action += 1
            return np.argmax(self.q_table[state])

    def update_q_table(self, reward, state, action):
        self.total_reward += reward
        self.q_table[state, action] = reward

    def new_episode(self):
        self.random_action = 0
        self.max_min_action = 0
        self.total_reward = 0