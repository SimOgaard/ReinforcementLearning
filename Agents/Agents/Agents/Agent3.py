import numpy as np

from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam

from collections import deque

from gym import spaces

class Agent3:
    def __init__(self, df, init_invest = 20000):
        self.action_space = spaces.Discrete(3)

        print(self.action_space)

        self.stock_price_history = np.around(df)
        self.stock_price_history.drop(5)

        print(self.stock_price_history)

        stock_max_price = self.stock_price_history.max(axis=1)
        price_range = [[0, mx] for mx in stock_max_price]

        print(stock_max_price)
        print(price_range)

        self.observation_space = spaces.MultiDiscrete(price_range)

        print(self.observation_space)