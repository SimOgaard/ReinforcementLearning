from gym.envs.registration import register

register(
    id='Market-v0',
    entry_point='MarketEnvironmentBasic.envs:Market_Basic',
)
