import numpy as np

from gym import spaces

class Agent3:
    def __init__(self, df):
        self.action_space = spaces.Discrete(3)

        print(self.action_space)

        self.stock_price_history = np.around(df.drop('Volume', axis=1))

        print(self.stock_price_history)

        stock_max_price = self.stock_price_history.max(axis=1)
        price_range = [[1, mx] for mx in stock_max_price]

        print(stock_max_price)
        print(price_range)

        self.observation_space = spaces.MultiDiscrete([price_range])

        print(self.observation_space)