import gym
from gym import error, spaces, utils
from gym.utils import seeding

class TicTac(gym.Env):
    metadata = {'render.modes': ['human']}
    
    def __init__(self):
        self.state = [[0,0,0],[0,0,0],[0,0,0]]
        self.done = False
        self.reward = 0
        self.turn = 0
    
    def check(self):
        for x in self.state:
            if x == [1,1,1]:
                return 1
            if x == [2,2,2]:
                return 2
        for y in list(zip(*reversed(self.state))):
            if y == (1,1,1):
                return 1
            if y == (2,2,2):
                return 2
        if self.state[0][2] == self.state[1][1] == self.state[2][0] == 1:
            return 1
        if self.state[0][2] == self.state[1][1] == self.state[2][0] == 2:
            return 2
        return 0

    def step(self, target):
        if self.state[int(target/3)][target%3]:
            print("invalid step")
            return [self.state, self.reward, self.done, self.turn]
        else:
            if not self.turn%2 == 0:
                self.state[int(target/3)][target%3] = 1
            else:
                self.state[int(target/3)][target%3] = 2
            self.turn += 1
            if self.turn == 9:
                self.done = True
        self.render()
        winner = self.check()
        if winner:
            self.done = True
            print("player", winner, "wins")
            if winner == 1:
                self.reward = 1
            else:
                self.reward = -1
        elif self.done:
            print("game over, no one won")
        return [self.state, self.reward, self.done, self.turn]

    def reset(self):
        self.__init__()
        return self.state

    def render(self):
        for x in self.state:
            print(x)
