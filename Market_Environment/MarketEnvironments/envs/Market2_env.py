import gym
from gym import error, spaces, utils
from gym.utils import seeding
import numpy as np
import matplotlib.pyplot as plt

class Market2(gym.Env):
    metadata = {'render.modes': ['human']}
    
    def __init__(self, df):
        self.prices = df.loc[:, 'Close'].to_numpy()
        self.max_index = self.prices.size
        self.selection = []

        self.trading_fee = 0.005
        self.state_index = 0
        self.last_value = 0
        self.done = False

        self.step(0)
        
    def step(self, target):
        self.this_value = self.prices[self.state_index]

        self.reward_rank, self.reward = self.get_reward(target)

        if self.reward_rank == 0:
            self.selection.append("green")
        elif self.reward_rank == 1:
            self.selection.append("yellow")
        else:
            self.selection.append("red")

        self.last_value = self.this_value
        self.state_index += 1

        self.done = self.max_index == self.state_index

        return [self.state_index, self.reward, self.done]

    def get_reward(self, target):
        buy_reward = (self.this_value - self.last_value)*2 - self.last_value * self.trading_fee
        hold_reward = self.this_value - self.last_value
        sell_reward = self.last_value - self.this_value - self.last_value * self.trading_fee

        reward_rank_list = [buy_reward, hold_reward, sell_reward]
        reward_rank_list.sort(reverse=True)

        if target == 0:
            reward = buy_reward
        elif target == 1:
            reward = hold_reward
        else:
            reward = sell_reward
        
        reward_rank = reward_rank_list.index(reward)

        return reward_rank, reward

    def reset(self):
        self.done = False
        self.state_index = 0
        self.last_value = 0
        self.selection = []
        self.step(0)
        return self.state_index

    def render(self):
        plt.plot(self.prices)
        for index_row in range(self.state_index):
            plt.plot(index_row, self.prices[index_row], marker=".", color=self.selection[index_row])
        plt.show()