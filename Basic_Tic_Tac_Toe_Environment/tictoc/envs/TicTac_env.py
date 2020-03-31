import gym
from gym import error, spaces, utils
from gym.utils import seeding
import numpy as np

class TicTac(gym.Env):
    metadata = {'render.modes': ['human']}
    
    def __init__(self):
        self.state = np.zeros((3,3))
        self.done = False
        self.reward = 0
        self.turn = 0
    
    def check(self):
        for x in range(3):
            if self.state[x] == [1,1,1]:
                return 1
            if self.state[x] == [2,2,2]:
                return 2
        rotated = np.rot90(self.state)
        for y in range(3):
            if self.state[y] == [1,1,1]:
                return 1
            if self.state[y] == [2,2,2]:
                return 2
        if self.state[0][2] == self.state[1][1] == self.state[2][0] == 1:
            return 1
        if self.state[0][2] == self.state[1][1] == self.state[2][0] == 2:
            return 2
        return 0

    def step(self, target):
        if self.done:
            print("game over")
        elif not self.state[int(target/3)][target%3]:
            if not self.turn%2 == 0:
                self.state[int(target/3)][target%3] = 1
            else:
                self.state[int(target/3)][target%3] = 2
            self.turn += 1
            if self.turn == 9:
                self.done == True
            self.render()
        else:
            print("invalid step")

        winner = self.check()
        if winner:
            self.done = True
            print("player", winner, "wins")
            if winner == 1:
                self.reward = 1
            else:
                self.reward = -1

        return [self.state, self.reward, self.done]

    def reset(self):
        self.__init__()

    def render(self):
        # render = self.state
        # render[render = 0] = " "
        # render[render = 1] = "x"
        # render[render = 2] = "o"
        # print(render)
        print(self.state)