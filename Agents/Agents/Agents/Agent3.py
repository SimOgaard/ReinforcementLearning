import numpy as np

from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam

from collections import deque

from gym import spaces

class Agent2:
    def __init__(self, df, init_invest = 20000):
        self.action_space = spaces.Discrete(3)

        print(self.action_space)

        self.stock_price_history = np.around(df)

        print(stock_price_history)

        stock_max_price = sef.stock_price_history.max(axis=1)
        stock_range = [[0, init_invest * 2 // mx] for mx in stock_max_price]
        price_range = [[0, mx] for mx in stock_max_price]
        cash_in_hand_range = [[0, init_invest * 2]]

        print(stock_max_price)
        print(stock_range)
        print(price_range)
        print(cash_in_hand_range)        

        self.observation_space = spaces.MultiDiscrete(stock_range + price_range + cash_in_hand_range)

        print(self.observation_space)