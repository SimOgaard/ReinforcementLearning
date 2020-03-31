from gym.envs.registration import register

register(
    id='Market-v1',
    entry_point='MarketEnvironmentMedium.envs:Market',
)