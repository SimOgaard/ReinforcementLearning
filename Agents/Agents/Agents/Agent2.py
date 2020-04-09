import numpy as np

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import Adam

from gym import spaces

class Agent2:
    
    def __init__(self, state_size, action_size, df):
        self.state_size = state_size
        self.action_size = action_size

        self.action_space = spaces.Discrete(self.action_size)
        self.stock_price_history = np.around(df.drop('Volume', axis=1))

        price_range = [[1, mx] for mx in self.stock_price_history.max(axis=1)]

        self.observation_space = spaces.MultiDiscrete([list(range(0, df.size))+price_range])

        self.random_action = 0
        self.mlp_action = 0
        self.total_reward = 0

        self.gamma = 0.1
        self.alpha = 0.1
        self.epsilon = 1
        self.epsilon_decay = 0.8

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
            self.mlp_action += 1
            print(state)
            print(self.model.predict(state))
            return np.argmax(self.model.predict(state)[0])

    def new_episode(self):
        self.random_action = 0
        self.mlp_action = 0
        self.total_reward = 0
        self.epsilon = self.epsilon * self.epsilon_decay

    def action_sample(self):
        self.random_action += 1
        return np.random.randint(self.action_size)