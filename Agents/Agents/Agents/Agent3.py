import numpy as np

import tensorflow.keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.models import load_model
from tensorflow.keras.models import save_model

from collections import deque

class Agent3:
    
    def __init__(self, action_size, df, day_memory):
        self.action_size = action_size
        self.day_memory = day_memory

        self.random_action = 0
        self.mlp_action = 0
        self.total_reward = 0

        self.gamma = 0.1
        self.epsilon = 1
        self.epsilon_decay = 0.995
        self.epsilon_min = 0.01

        self.model = self.mlp()
        self.memory = deque(maxlen=2000)

    def mlp(self):
        model = Sequential()
        model.add(Dense(units=64, input_dim=self.day_memory*5, activation="relu"))
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
            self.mlp_action += 1
            try:
                options = self.model.predict(state)
            except:
                # print("Error: State:",state)
                return np.random.randint(self.action_size)
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
            target = reward

            if not done:
                target = reward + self.gamma * np.amax(self.model.predict(next_state)[0])

            target_f = self.model.predict(state)
            target_f[0][action] = target
            self.model.fit(state, target_f, epochs=1, verbose=0)
            
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay 

    def load_model(self, model_name):
        self.model = load_model("/content/ReinforcementLearning/models/" + model_name)

    def save_model(self, model_name):
        save_model("/content/ReinforcementLearning/models/" + model_name)