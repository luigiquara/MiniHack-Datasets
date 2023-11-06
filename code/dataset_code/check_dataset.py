# Simple script to check a dataset
# Pick n index at random and print the tty_render
# To control that everything is ok, i.e. not empty frames

import argparse
import random
import pickle
from nle.nethack import tty_render

parser = argparse.ArgumentParser()
parser.add_argument(
    '--path',
    type=str
)
flags = parser.parse_args()
path = flags.path

with open(path+'.pkl', 'rb') as f: dataset = pickle.load(f)
print(f'loaded {path}')

# n spot checks
for i in range(10):
    index = random.randrange(len(dataset))
    print(tty_render(dataset[index]['chars'], dataset[index]['colors']))
    print(f'index: {index}')
    input('press any key to continue')