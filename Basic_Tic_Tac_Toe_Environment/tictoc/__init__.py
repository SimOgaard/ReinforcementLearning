from gym.envs.registration import register

register(
    id='TicTac-v0',
    entry_point='tictoc.envs:TicTac',
)
