# MiniHack-Datasets

Collection of dataset for some MiniHack environments, *i.e.* **River**, **WandOfDeath-Medium**, **Quest-Easy**.
Each dataset is a collection of frames from a specific environment.<br/>
The frames come from the experiences of some agents, namely a random agent, a "*programmed*" one.

### Organization of the repo
**Agents**<br/>
Contains the implementation of a random agent and a "*programmed*" one for the `River` environment.<br/>
For the `WoD-Medium` and `Quest-Easy` environment, we collected games from human players.<br/>
`run_and_play.py` is the script to let the agents play and collect the frames.<br/>

We collected about 10k frames for each environment and type of agent. <br/>
`dataset.pkl` is the concatenation of the env-specific datasets.<br/>
It contains about 60k frames.
