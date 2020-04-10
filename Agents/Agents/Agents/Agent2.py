import numpy as np
import math

import tensorflow.keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import Adam

from gym import spaces
from collections import deque

class Agent2:
    
    def __init__(self, action_size, df, day_memory):
        self.action_size = action_size
        self.day_memory = day_memory
        
        stock_wo_volume = df.drop('Volume', axis=1)
        stock_price_history = np.around(stock_wo_volume)
        price_range = [[1, mx] for mx in stock_price_history.max(axis=1)]

        self.random_action = 0
        self.mlp_action = 0
        self.total_reward = 0

        self.gamma = 0.1
        self.alpha = 0.1
        self.epsilon = 1
        self.epsilon_decay = 0.95
        self.epsilon_min = 0.01

        self.data = df['Close'].tolist()
        # self.data = self.get_stock_data_vec(df)
        self.model = self.mlp()
        self.memory = deque(maxlen=1000)

    def mlp(self):
        model = Sequential()
        model.add(Dense(units=64, input_dim=self.day_memory, activation="relu"))
        model.add(Dense(units=32, activation="relu"))
        model.add(Dense(units=8, activation="relu"))
        model.add(Dense(self.action_size, activation="linear"))
        model.compile(loss="mse", optimizer=Adam(lr=0.001))
        return model

    def get_stock_data_vec(self, data):
        vec = []
        for index in data[:][1:]:
            print(index)
            vec.append(index[4])
        return vec

    def sigmoid(self, x):
        return 1 / (1 + math.exp(-x))

    def get_state(self, data, t, n):
        n+=1
        d = t - n + 1
        block = data[d:t + 1] if d >= 0 else -d * [data[0]] + data[0:t + 1]
        res = []
        for i in range(n-1):
            res.append(self.sigmoid(block[i + 1] - block[i]))
        return np.array([res])

    def act(self, state):

        self.state = self.get_state(self.data, state, self.day_memory) # backwards compadible with other environments

        if np.random.rand() < self.epsilon:
            self.random_action += 1
            return np.random.randint(self.action_size)
        else:
            self.mlp_action += 1
            options = self.model.predict(self.state)
            return np.argmax(options[0])

    def new_episode(self):
        self.random_action = 0
        self.mlp_action = 0
        self.total_reward = 0

    def exp_replay(self, batch_size):
        mini_batch = []
        l = len(self.memory)
        for i in range(l - batch_size + 1, l):
            mini_batch.append(self.memory[i])

        for state, action, reward, next_state, done in mini_batch:
            print(state, action, reward, next_state, done)
            target = reward
            
            if not done:
                target = reward + self.gamma * np.amax(self.model.predict(next_state)[0])
            
            target_f = self.model.predict(state)
            target_f[0][action] = target
            self.model.fit(state, target_f, epochs=1, verbose=0)

        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay 
