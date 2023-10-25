import numpy as np

class WoDAgent():
    def __init__(self, env):
        self.env = env
        self.reset()

    def reset(self):
        self.has_wand = False
        self.minotaur_dead = False

    def process_obs(self, obs):
        # get the position of the agent
        agent_row, agent_col = np.where(obs['chars'] == ord('@'))
        self.agent_pos = (agent_row[0], agent_col[0])

        if self.has_wand: self.on_wand = False

        if not self.has_wand:
            # get the position of wand
            wand_row, wand_col = np.where(obs['chars'] == ord('/'))
            if wand_row:
                self.wand_pos = (wand_row[0], wand_col[0])
            else: self.wand_pos = None

            # check if you're stepping on the wand
            if self.wand_pos == None:
                message = bytes(obs['message']).decode('utf-8').rstrip('\x00')
                if 'You see here' in message and 'wand' in message:
                    self.on_wand = True
                    self.has_wand = True
                else: self.on_wand = False

        # check if the minotaur is dead
        if not self.minotaur_dead:
            corpse_row, corpse_col = np.where(obs['chars'] == ord('%'))
            if corpse_row:
                self.minotaur_dead = True
                self.distance = 99999 # infinite distance since it is dead
            else: self.minotaur_dead = False

        # lastly, get the distance from the minotaur
        if not self.minotaur_dead:
            minotaur_row, minotaur_col = np.where(obs['chars'] == ord('H'))
            self.minotaur_pos = (minotaur_row[0], minotaur_col[0])
            self.distance = abs(self.agent_pos[1] - self.minotaur_pos[1])

    def take_action(self, obs):
        # if you see the wand, go towards it
        # if you're on the wand, pick it
        # if you're near the minotaur (less than 6 cells), zap
        # if the minotaur is dead, go to the exit

        self.process_obs(obs)
        action = None

        if self.wand_pos:
            # TODO: go towards the wand
            if self.wand_pos[1] > self.agent_pos[1]: action = 'east'
            else: action = 'west'

        elif self.on_wand: action = 'pickup'
        elif self.distance < 6: action = 'zap'
        else: action ='east' # go towards the exit

        if action == None: print('uhmm, maybe there is a problem')
        return action