import argparse
import pickle

import pandas as pd
import numpy as np

from collections import Counter

# create a counter object
# count the occurencies of all (char, color) tuples
def create_counter(path):
    with open(path+'.pkl', 'rb') as f: dataset = pickle.load(f)
    chars = np.array([frame['chars'] for frame in dataset]).flatten()
    colors = np.array([frame['colors'] for frame in dataset]).flatten()
    #glyphs = np.array(I[frame['glyphs'] for frame in dataset]).flatten()

    #ch_co_gl = list(zip(chars, colors, glyphs))
    ch_co = list(zip(chars, colors))
    counter = Counter(ch_co) 
    with open(path+'.counter', 'wb') as f: pickle.dump(counter, f)

    return counter

# from nle.nethack.tty_render
def create_ANSI(char, color):
    entry = "\033[%d;3%dm%s" % (
                # & 8 checks for brightness.
                bool(color & 8),
                color & ~8,
                chr(char),
            )
    return entry

# descriptions from nethack guidebook
def create_description(char_ascii):
    char_to_des = {
       ord('-'): 'Walls - open door or grave',
       ord('|'): 'Walls - open door or grave',
       ord('.'): 'Floor - ice or doorless doorway',
       ord('#'): 'Corridor - iron bars-tree-kitchen sink-drawbridge',
       ord('>'): 'DownStairs',
       ord('<'): 'UpStairs',
       ord('+'): 'ClosedDoor - spellbook',
       ord('@'): 'You - human',
       ord('$'): 'Gold',
       ord('^'): 'Trap',
       ord(')'): 'Weapon',
       ord('['): 'Suit - armor',
       ord('%'): 'Edible',
       ord('?'): 'Scroll',
       ord('/'): 'Wand',
       ord('='): 'Ring',
       ord('!'): 'Potion',
       ord('('): 'UsefulItem',
       ord('"'): 'Amulet - spider web',
       ord('*'): 'Gem - rock',
       ord('`'): 'Boulder - statue',
       ord('0'): 'IronBall', #missing from current dataset
       ord('_'): 'Altar - iron chair',
       ord('{'): 'Fountain',
       ord('}'): 'WaterPool - LavaPool - moat',
       ord('\\'): 'Throne',
    }

    # ' are golems
    # : are lizards
    if chr(char_ascii).isalpha() or char_ascii == ord("'") or char_ascii == ord(':') or char_ascii == ord('&'):
        return 'Inhabitant' 
    elif chr(char_ascii) == ' ' or chr(char_ascii) == '\x00':
        return 'Void'
    else:
        try:
            return char_to_des[char_ascii]
        except KeyError:
            print(f'KeyError {chr(char_ascii)}')
            return 'Unknown'

def create_dataframe(counter, path):
    # add (chars,colors) and number of occurences
    chars, colors = list(zip(*list(counter.keys())))
    df = pd.DataFrame(list(zip(chars, colors, counter.values())), columns=['char', 'color', 'frequency'])
    df.sort_values(by='frequency', ascending=False, ignore_index=True, inplace=True)

    # add graphical glyphs
    ansi_codes = list(map(create_ANSI, df['char'], df['color']))
    df['icon'] = ansi_codes

    # add textual descriptions
    descriptions = list(map(create_description, df['char'])) 
    df['description'] = descriptions
    
    # saving
    df.to_pickle(path+'.df')
    return df

# group all rows with the same description and
# aggregate them (sum frequencies and pick most common (char, color) value)
# to get macro-classes
def group_df(df, path):
    aggregation_functions = {'frequency': 'sum', 'char': 'first', 'color': 'first', 'icon': 'first'}
    grouped_df = df.groupby(['description']).aggregate(aggregation_functions)
    grouped_df['relative_frequency'] = grouped_df['frequency']*100/grouped_df['frequency'].sum()

    grouped_df.sort_values('frequency', ascending=False, inplace=True)
    grouped_df['id'] = range(0, len(grouped_df))
    grouped_df.to_pickle(path+'.grouped_df')
    return grouped_df

def main(path):
    try:
        with open(path+'.counter', 'rb') as f:
            print(f'Reading counter from {path}')
            counter = pickle.load(f)
    except:
        print(f'Creating counter for {path}')
        counter = create_counter(path)

    try:
        df = pd.read_pickle(path+'.df')
        print(f'Reading DataFrame from {path}')
    except:
        print(f'Creating DataFrame for {path}')
        df = create_dataframe(counter, path)

    try:
        grouped_df = pd.read_pickle(path+'.grouped_df')
        print(f'Reading Grouped DataFrame from {path}')
    except:
        print(f'Creating Grouped DataFrame for {path}')
        grouped_df = group_df(df, path)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--path',
        type=str,
        help='The path to the dataset'
    )

    flags = parser.parse_args()
    main(**vars(flags))