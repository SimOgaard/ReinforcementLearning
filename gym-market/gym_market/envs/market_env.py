import gym
from gym import error, spaces, utils
from gym.utils import seeding

import glob
import os
import random

import pandas as pd
import numpy as np

ACTION_SKIP = 0
ACTION_BUY = 1
ACTION_SELL = 2

class MarketState:
    def __init__(self, equity_path, sep=','):
        df = self.read_csv(equity_path, sep=sep)

        df = df.fillna(method='ffill')
        df = df.fillna(method='bfill')

        self.df = df
        self.index = 0

        print("Imported tick data from {}".format(equity_path))

    def read_csv(self, path, sep):
        dtypes = {'Date': str, 'Time': str}
        df = pd.read_csv(path, sep=sep, header=0, names=['Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume'], dtype=dtypes)
        dtime = df.Date + ' ' + df.Time
        df.index = pd.to_datetime(dtime)
        df.drop(['Date', 'Time'], axis=1, inplace=True)
        return df

    def reset(self):
        self.index = 0

    def next(self):
        if self.index >= len(self.df) - 1:
            return None, True

        values = self.df.iloc[self.index].values

        self.index += 1

        return values, False

    def shape(self):
        return self.df.shape

    def current_price(self):
        return self.df.ix[self.index, 'Close']

class Market(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self, datadir):
        self.bound = 100000

        self.comission = 0.1 / 100.
        self.num = 1

        self.money = 0
        self.equity = 0
        self.states = []
        self.state = None

        for path in glob.glob(datadir + '/*.csv'):
            if not os.path.isfile(path):
                continue

            self.states.append(path)

        self.observation_space = spaces.Box(low=0, high=self.bound, shape=(5,1))
        self.action_space = spaces.Discrete(3)

        if len(self.states) == 0:
            raise NameError('Invalid empty directory {}'.format(dirname))

    def _step(self, action):
        assert self.action_space.contains(action)

        portfolio = self.money + (1. - self.comission) * self.equity * self.state.current_price()
        price = self.state.current_price()
        cost = price * self.num
        comission_price = cost * (1. + self.comission)
        equity_price = price * self.equity
        prev_portfolio = self.money + equity_price

        if action == ACTION_BUY:
            if self.money >= comission_price:
                self.money -= comission_price
                self.equity += self.num
        if action == ACTION_SELL:
            if self.equity > 0:
                self.money += (1. - self.comission) * cost
                self.equity -= self.num

        state, done = self.state.next()

        new_price = price
        if not done:
            new_price = self.state.current_price()

        new_equity_price = new_price * self.equity
        reward = (self.money + new_equity_price) - prev_portfolio

        return state, reward, done, None

    def _reset(self):
        self.state = MarketState(random.choice(self.states))

        self.money = 1000000
        self.equity = 0

        state, done = self.state.next()
        return state

    def _render(self, mode='human', close=False):
        pass

# import random
# import json
# import gym
# from gym import spaces
# import pandas as pd
# import numpy as np

# MAX_ACCOUNT_BALANCE = 2147483647
# MAX_NUM_SHARES = 2147483647
# MAX_SHARE_PRICE = 5000
# MAX_OPEN_POSITIONS = 5
# MAX_STEPS = 20000

# INITIAL_ACCOUNT_BALANCE = 10000

# class Market(gym.Env):
#     metadata = {'render.modes': ['human']}

#     def __init__(self, df):
#         super(Market, self).__init__()

#         self.df = df
#         self.reward_range = (0, MAX_ACCOUNT_BALANCE)

#         # Actions of the format Buy x%, Sell x%, Hold, etc.
#         self.action_space = spaces.Box(low=np.array([0, 0]), high=np.array([3, 1]), dtype=np.float16)

#         # Prices contains the OHCL values for the last five prices
#         self.observation_space = spaces.Box(low=0, high=1, shape=(6, 6), dtype=np.float16)

#     def _next_observation(self):
#         # Get the stock data points for the last 5 days and scale to between 0-1
#         frame = np.array([
#             self.df.loc[self.current_step: self.current_step + 5, 'Open'].values / MAX_SHARE_PRICE,
#             self.df.loc[self.current_step: self.current_step + 5, 'High'].values / MAX_SHARE_PRICE,
#             self.df.loc[self.current_step: self.current_step + 5, 'Low'].values / MAX_SHARE_PRICE,
#             self.df.loc[self.current_step: self.current_step + 5, 'Close'].values / MAX_SHARE_PRICE,
#             self.df.loc[self.current_step: self.current_step + 5, 'Volume'].values / MAX_NUM_SHARES,
#         ])

#         # Append additional data and scale each value to between 0-1
#         obs = np.append(frame, [[
#             self.balance / MAX_ACCOUNT_BALANCE,
#             self.max_net_worth / MAX_ACCOUNT_BALANCE,
#             self.shares_held / MAX_NUM_SHARES,
#             self.cost_basis / MAX_SHARE_PRICE,
#             self.total_shares_sold / MAX_NUM_SHARES,
#             self.total_sales_value / (MAX_NUM_SHARES * MAX_SHARE_PRICE),
#         ]], axis=0)

#         return obs

#     def _take_action(self, action):
#         # Set the current price to a random price within the time step
#         current_price = random.uniform(self.df.loc[self.current_step, "Open"], self.df.loc[self.current_step, "Close"])

#         action_type = action[0]
#         amount = action[1]

#         if action_type < 1:
#             # Buy amount % of balance in shares
#             total_possible = int(self.balance / current_price)
#             shares_bought = int(total_possible * amount)
#             prev_cost = self.cost_basis * self.shares_held
#             additional_cost = shares_bought * current_price

#             self.balance -= additional_cost
#             self.cost_basis = (prev_cost + additional_cost) / (self.shares_held + shares_bought)
#             self.shares_held += shares_bought

#         elif action_type < 2:
#             # Sell amount % of shares held
#             shares_sold = int(self.shares_held * amount)
#             self.balance += shares_sold * current_price
#             self.shares_held -= shares_sold
#             self.total_shares_sold += shares_sold
#             self.total_sales_value += shares_sold * current_price

#         self.net_worth = self.balance + self.shares_held * current_price

#         if self.net_worth > self.max_net_worth:
#             self.max_net_worth = self.net_worth

#         if self.shares_held == 0:
#             self.cost_basis = 0

#     def step(self, action):
#         # Execute one time step within the environment
#         self._take_action(action)

#         self.current_step += 1

#         if self.current_step > len(self.df.loc[:, 'Open'].values) - 6:
#             self.current_step = 0

#         delay_modifier = (self.current_step / MAX_STEPS)

#         reward = self.balance * delay_modifier
#         done = self.net_worth <= 0

#         obs = self._next_observation()

#         return obs, reward, done, {}

#     def reset(self):
#         # Reset the state of the environment to an initial state
#         self.balance = INITIAL_ACCOUNT_BALANCE
#         self.net_worth = INITIAL_ACCOUNT_BALANCE
#         self.max_net_worth = INITIAL_ACCOUNT_BALANCE
#         self.shares_held = 0
#         self.cost_basis = 0
#         self.total_shares_sold = 0
#         self.total_sales_value = 0

#         # Set the current step to a random point within the data frame
#         self.current_step = random.randint(0, len(self.df.loc[:, 'Open'].values) - 6)

#         return self._next_observation()

#     def render(self, mode='human', close=False):
#         # Render the environment to the screen
#         profit = self.net_worth - INITIAL_ACCOUNT_BALANCE

#         print(f'Step: {self.current_step}')
#         print(f'Balance: {self.balance}')
#         print(
#             f'Shares held: {self.shares_held} (Total sold: {self.total_shares_sold})')
#         print(
#             f'Avg cost for held shares: {self.cost_basis} (Total sales value: {self.total_sales_value})')
#         print(
#             f'Net worth: {self.net_worth} (Max net worth: {self.max_net_worth})')
#         print(f'Profit: {profit}')

# import gym
# from gym import error, spaces, utils
# from gym.utils import seeding

# class Market(gym.Env):
#     metadata = {'render.modes': ['human']}

#     def __init__(self):
#         self.state = []
#         for i in range(3):
#             self.state += [[]]
#             for j in range(3):
#                 self.state[i] += ["-"]
#         self.counter = 0
#         self.done = 0
#         self.add = [0, 0]
#         self.reward = 0

#     def check(self):
#         if(self.counter<5):
#             return 0
#         for i in range(3):
#             if(self.state[i][0] != "-" and self.state[i][1] == self.state[i][0] and self.state[i][1] == self.state[i][2]):
#                 if(self.state[i][0] == "o"):
#                     return 1
#                 else:
#                     return 2
#             if(self.state[0][i] != "-" and self.state[1][i] == self.state[0][i] and self.state[1][i] == self.state[2][i]):
#                 if(self.state[0][i] == "o"):
#                     return 1
#                 else:
#                     return 2
#         if(self.state[0][0] != "-" and self.state[1][1] == self.state[0][0] and self.state[1][1] == self.state[2][2]):
#             if(self.state[0][0] == "o"):
#                 return 1
#             else:
#                 return 2
#         if(self.state[0][2] != "-" and self.state[0][2] == self.state[1][1] and self.state[1][1] == self.state[2][0]):
#             if(self.state[1][1] == "o"):
#                 return 1
#             else:
#                 return 2

#     def step(self, target):
#         if self.done == 1:
#             print("Game Over")
#             return [self.state, self.reward, self.done, self.add]
#         elif self.state[int(target/3)][target%3] != "-":
#             print("Invalid Step")
#             return [self.state, self.reward, self.done, self.add]
#         else:
#             if(self.counter%2 == 0):
#                 self.state[int(target/3)][target%3] = "o"
#             else:
#                 self.state[int(target/3)][target%3] = "x"
#             self.counter += 1
#             if(self.counter == 9):
#                 self.done = 1;
#             self.render()

#         win = self.check()
#         if(win):
#             self.done = 1;
#             print("Player ", win, " wins.", sep = "", end = "\n")
#             self.add[win-1] = 1;
#             if win == 1:
#                 self.reward = 100
#             else:
#                 self.reward = -100

#         return [self.state, self.reward, self.done, self.add]

#     def reset(self):
#         for i in range(3):
#             for j in range(3):
#                 self.state[i][j] = "-"
#         self.counter = 0
#         self.done = 0
#         self.add = [0, 0]
#         self.reward = 0
#         return self.state

#     def render(self):
#         for i in range(3):
#             for j in range(3):
#                 print(self.state[i][j], end = " ")
#             print("")