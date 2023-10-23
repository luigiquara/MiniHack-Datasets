import argparse
import gym
import minihack

from random_agent import RandomAgent
from river_agent import RiverAgent
from wod_agent import WoDAgent
from quest_agent import QuestAgent

def main(env, random_agent, num_episodes, max_steps, path):
    env = gym.make(env)
    # TODO: save obs in an array and then write it to file
    obs = env.reset()

    if random_agent: agent = RandomAgent(env)
    elif 'River' in env: agent = RiverAgent(env)
    elif 'WoD' in env: agent = WoDAgent(env)
    elif 'Quest' in env: agent = QuestAgent(env)
    else: raise Exception('Unexpected environment') 

    for i in range(num_episodes):
        for s in range(max_steps):
            if done: break

            action = agent.take_action(obs)
            # TODO: check return of env.step
            obs, done = env.step(action)



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--env',
        type=str,
        help='The environment to use'
    )
    parser.add_argument(
        '--random',
        action='store_true',
        help='Use the random agent'
    )
    parser.add_argument(
        '--no-random',
        action='store_false',
        dest='random',
        help='Use the programmed agent'
    ),
    parser.add_argument(
        '--num_episodes',
        type=int,
        default=30
        help='Number of episodes to run'
    )
    parser.add_argument(
        '--max_steps',
        type=int,
        default=100,
        help='Maximum number of steps per episode'
    )
    parser.add_argument(
        '--path',
        type=str,
        help='Where to save the frames'
    )

    flags = parser.parse_args()
    main(**vars(flags))