import random

class RandomAgent():
    def __init__(self, env):
        self.env = env
        self.action_space = len(env.actions)

    def take_action(self, obs):
        action_id = random.randrange(0, self.action_space)
        return action_id

    # just for compatibility with other agents
    def reset(self): return