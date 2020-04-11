import gym
from gym import error, spaces, utils
from gym.utils import seeding
import numpy as np
import matplotlib.pyplot as plt

class Market2(gym.Env):
    metadata = {'render.modes': ['human']}
    
    def __init__(self, df):
        prices = df.drop('Volume', axis=1)
        self.prices = prices.loc[:, ["High":"Close", "Adj Close"]].to_numpy()
        self.max_index = self.prices.size-1
        self.selection_plot = []
        self.reward_plot = []

        self.action_size = 3
        self.trading_fee = 0.005
        self.state_index = 0
        self.done = False
        
    def step(self, target):
        self.this_reward_value = self.prices[self.state_index, "Close"]
        self.next_reward_value = self.prices[self.state_index+1, "Close"]

        self.reward = self.get_reward(target)

        self.state_index += 1

        self.done = self.max_index == self.state_index

        return [self.state_index, self.reward, self.done, self.prices[self.state_index]]

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

    def get_reward(self, target):
        buy_reward = (self.next_reward_value - self.this_reward_value)*2 - self.this_reward_value * self.trading_fee
        hold_reward = self.next_reward_value - self.this_reward_value
        sell_reward = self.this_reward_value - self.next_reward_value - self.this_reward_value * self.trading_fee

        if target == 0:
            self.selection_plot.append("green")
            reward = buy_reward
        elif target == 1:
            self.selection_plot.append("yellow")
            reward = hold_reward
        else:
            self.selection_plot.append("red")
            reward = sell_reward

        reward_rank_list = [buy_reward, hold_reward, sell_reward]
        reward_rank_list.sort(reverse=True)
        reward_rank = reward_rank_list.index(reward)

        if reward_rank == 0:
            self.reward_plot.append("green")
        elif reward_rank == 1:
            self.reward_plot.append("yellow")
        else:
            self.reward_plot.append("red")

        return reward

    def reset(self):
        self.done = False
        self.state_index = 0
        self.selection_plot = []
        self.reward_plot = []
        return self.state_index

    def render(self, plots, title):
        plt.plot(self.prices)
        plt.title(title)
        for index_row in range(self.state_index):
            plt.plot(index_row, self.prices[index_row], marker=".", color=plots[index_row])
        plt.show()