import argparse
import pickle

import gym
import minihack

from random_agent import RandomAgent
#from river_agent import RiverAgent
from wod_agent import WoDAgent
#from quest_agent import QuestAgent

def perform_action(action, env):
    if isinstance(action, int): action_id = action
    else:
        if action == 'pickup': action_id = 49
        if action == 'zap':
            action_id = 80
            obs, _,_,_ = env.step(action_id)
            # Example message:
            # What do you want to zap?[f or *]
            message = bytes(obs['message']).decode('utf-8').rstrip('\x00')
            wand_char = message.split('[')[1][0] # Because of the way the message in NetHack works
            action_id = env.actions.index(ord(wand_char))
            obs, _,_,_ = env.step(action_id)
            # Next message:
            # In what direction?
            action_id = 1 # Minotaur is always east

        # Movement actions
        elif 'northeast' in action: action_id = 4
        elif 'southeast' in action: action_id = 5
        elif 'southwest' in action: action_id = 6
        elif 'northwest' in action: action_id = 7
        elif 'north' in action: action_id = 0
        elif 'east' in action: action_id = 1
        elif 'south' in action: action_id = 2
        elif 'west' in action: action_id = 3

    obs, reward, done, info = env.step(action_id)
    return obs, reward, done, info


def main(env_name, random_agent, num_episodes, max_steps, path, fast_mode):
    env = gym.make('MiniHack-'+env_name+'-v0', observation_keys=['glyphs', 'chars', 'colors', 'message'])
    global obs
    obs = []

    if random_agent: agent = RandomAgent(env)
    elif 'River' in env_name: agent = RiverAgent(env)
    elif 'WoD' in env_name: agent = WoDAgent(env)
    elif 'Quest' in env_name: agent = QuestAgent(env)
    else: raise Exception('Unexpected environment') 

    for episode in range(num_episodes):
        mean_reward = 0.0

        o = env.reset()
        agent.reset()
        obs.append(o)
        if not fast_mode:
            env.render()
            input('Press any key to continue')

        for step in range(max_steps):
            action = agent.take_action(o)
            if not fast_mode: print(f'Action: {action}')
            o, reward, done, info = perform_action(action, env)
            obs.append(o)

            mean_reward = (reward - mean_reward) / (step + 1)

            if not fast_mode:
                env.render()
                input('Press any key to continue')

            if done: break

        # Print information about the ended episode
        print(f'Episode {episode} - {step+1} steps')
        print(f'End status: {info["end_status"].name}')
        print(f'Final reward: {reward}')
        print(f'Mean reward: {mean_reward}')

    
    with open(path+'.pkl', 'wb') as f: pickle.dump(obs, f)



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--env',
        type=str,
        dest='env_name',
        help='The environment to use'
    )
    parser.add_argument(
        '--random',
        action='store_true',
        dest='random_agent',
        help='Use the random agent'
    )
    parser.add_argument(
        '--no-random',
        action='store_false',
        dest='random_agent',
        help='Use the programmed agent'
    )
    parser.add_argument(
        '--num_episodes',
        type=int,
        default=30,
        help='Number of episodes to run'
    )
    parser.add_argument(
        '--max_steps',
        type=int,
        default=30,
        help='Maximum number of steps per episode'
    )
    parser.add_argument(
        '--path',
        type=str,
        help='Where to save the frames'
    )
    parser.add_argument(
        '--fast_mode',
        action='store_true',
        help='Print only summary information'
    )

    flags = parser.parse_args()
    main(**vars(flags))