# MiniHack Datasets
This repo is a collection of the scripts needed to generate the dataset.<br/>
The dataset is a list of frames from three MiniHack environments, *i.e.* **River**, **Wand of Death - Medium** and **Quest - Easy**.<br/>
Each frame is a dictionary, which represents an observation from the environment. It contains the `chars` and `colors` keys, as long as other information.

We collected the observations from the experiences of a random agent, a "*programmed*" one and a human player.<br/>
For each environment, we saved about 10k frames per type of agent. In particular:

+ **River**: $\sim$ 10k frames by a random agent (200 episodes, 50 max_steps) - $\sim$ 10k frames by a human player (about 120 games);
+ **Wand of Death - Medium**: $\sim$ 10k frames by a random agent (200 episodes, 50 max_steps) - $\sim$ 10k frames by a "*programmed*" agent (350 episodes, 50 max_steps);
+ **Quest - Easy**: $\sim$ 10k frames by a random agent (220 episodes, 50 max_steps) - $\sim$ 11k frames by a human player (about 270 games).

We then take the entire dataset as the concatenation of the frames per each environment. `dataset.pkl` contains about 62k frames.


### Organization of the repo
`run_and_play.py` is the script to let the agents play and collect the frames.<br/>
`create_df.py` is the script that creates a pandas DataFrame for the dataset, to analyze its data; it also creates a "grouped" DataFrame, where entities with the same description (*i.e.* belonging to the same NetHack *macro-class*) are put together.
