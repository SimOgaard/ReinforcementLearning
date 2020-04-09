import numpy as np

import tensorflow.keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import Adam

from gym import spaces

import math

# from collections import deque

class Agent2:
    
    def __init__(self, state_size, action_size, df):
        self.state_size = state_size
        self.action_size = action_size

        self.action_space = spaces.Discrete(self.action_size)
        self.stock_price_history = np.around(df.drop('Volume', axis=1))

        price_range = [[1, mx] for mx in self.stock_price_history.max(axis=1)]

        self.observation_space = spaces.MultiDiscrete([price_range])

        self.random_action = 0
        self.mlp_action = 0
        self.total_reward = 0

        self.gamma = 0.1
        self.alpha = 0.1
        self.epsilon = 1
        self.epsilon_decay = 0.8

        self.data = self.getStockDataVec("stock_name")

        self.model = self.mlp()


        # self.memory = deque(maxlen=1000)

    def mlp(self):
        model = Sequential()
        model.add(Dense(units=64, input_dim=5, activation="relu"))
        model.add(Dense(units=32, activation="relu"))
        model.add(Dense(units=8, activation="relu"))
        model.add(Dense(3, activation="linear"))
        model.compile(loss="mse", optimizer=Adam(lr=0.001))
        return model

    def getStockDataVec(self, key):
        vec = []
        lines = open("/content/ReinforcementLearning/DataMarket/data/MMM.csv", "r").read().splitlines()

        for line in lines[1:]:
            vec.append(float(line.split(",")[4]))

        return vec

    def sigmoid(self, x):
        return 1 / (1 + math.exp(-x))

    def getState(self, data, t, n):
        # print("l")
        d = t - n + 1
        # print("a")
        block = data[d:t + 1] if d >= 0 else -d * [data[0]] + data[0:t + 1] # pad with t0
        # print("m")
        res = []
        for i in range(n - 1):
            # print("a")
            res.append(self.sigmoid(block[i + 1] - block[i]))
        # print("a")
        # print(res)
        return np.array([res])

    def act(self, state):

        self.state = self.getState(self.data, state, 6)
        # agent.memory.append((state, action, reward, next_state, done))

        if np.random.rand() < self.epsilon:
            self.random_action += 1
            return np.random.randint(self.action_size)
        else:
            self.mlp_action += 1
            # print("self.state",self.state)
            # print(self.model.predict(self.state))
            # return np.argmax(self.model.predict(self.state)[0])
            options = self.model.predict(self.state)
            # print("options",options)
            return np.argmax(options[0])

    def new_episode(self):
        self.random_action = 0
        self.mlp_action = 0
        self.total_reward = 0
        self.epsilon = self.epsilon * self.epsilon_decay

    def action_sample(self):
        self.random_action += 1
        return np.random.randint(self.action_size)




    # def expReplay(self, batch_size):
    #     mini_batch = []
    #     l = len(self.memory)
    #     for i in range(l - batch_size + 1, l):
    #         mini_batch.append(self.memory[i])
        
    #     for state, action, reward, next_state, done in mini_batch:
    #         target = reward
    #         if not done:
    #             target = reward + self.gamma * np.amax(self.model.predict(next_state)[0])
            
    #         target_f = self.model.predict(state)
    #         target_f[0][action] = target
    #         self.model.fit(state, target_f, epochs=1, verbose=0)
        
    #     if self.epsilon > self.epsilon_min:
    #         self.epsilon *= self.epsilon_decay 
