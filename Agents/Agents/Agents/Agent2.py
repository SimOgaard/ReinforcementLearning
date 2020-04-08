import numpy as np

from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam

from collections import deque

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

        self.memory = deque(maxlen=1000)
        self.model = self.mlp()

    def mlp(self):
        model = Sequential()
		model.add(Dense(units=64, input_dim=self.state_size, activation="relu"))
		model.add(Dense(units=32, activation="relu"))
		model.add(Dense(units=8, activation="relu"))
		model.add(Dense(self.action_size, activation="linear"))
		model.compile(loss="mse", optimizer=Adam(lr=0.001))
        return model

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
        self.epsilon = self.epsilon * self.epsilon_decay

    def action_sample(self):
        self.random_action += 1
        return np.random.randint(self.action_size)