from gym.envs.registration import register

register(
    id='Market-v0',
    entry_point='MarketEnvironments.envs:Market0',
)

register(
    id='Market-v1',
    entry_point='MarketEnvironments.envs:Market1',
)

register(
    id='Market-v2',
    entry_point='MarketEnvironments.envs:Market2',
)