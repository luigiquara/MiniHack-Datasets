import pickle

def add_env_agent(dataset, env, agent_mode):
    for frame in dataset:
        frame['env'] = env
        frame['agent_mode'] = agent_mode

dir = '/home/lquarantiello/minihack_datasets/dataset/'

with open(dir+'river/human_agent.pkl', 'rb') as f: river_human = pickle.load(f)
add_env_agent(river_human, 'river', 'human')
with open(dir+'river/random_agent.pkl', 'rb') as f: river_random = pickle.load(f)
add_env_agent(river_random, 'river', 'random')

with open(dir+'quest_easy/human_agent.pkl', 'rb') as f: quest_human = pickle.load(f)
add_env_agent(quest_human, 'quest', 'human')
with open(dir+'quest_easy/random_agent.pkl', 'rb') as f: quest_random = pickle.load(f)
add_env_agent(quest_random, 'quest', 'random')

with open(dir+'wod_medium/programmed_agent.pkl', 'rb') as f: wod_programmed = pickle.load(f)
add_env_agent(wod_programmed, 'wod', 'programmed')
with open(dir+'wod_medium/random_agent.pkl', 'rb') as f: wod_random = pickle.load(f)
add_env_agent(wod_random, 'wod', 'random')

dataset = []
dataset.extend(river_human)
dataset.extend(river_random)
dataset.extend(quest_human)
dataset.extend(quest_random)
dataset.extend(wod_programmed)
dataset.extend(wod_random)

assert len(dataset) == len(river_human)+len(river_random)+len(quest_human)+len(quest_random)+len(wod_programmed)+len(wod_random)

with open(dir+'dataset.pkl', 'wb') as f: pickle.dump(dataset, f)