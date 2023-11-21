from tqdm import tqdm
import pickle
import numpy as np
import pandas
from sklearn.model_selection import train_test_split as tts

# detect the uniform frames, i.e. where all characters are the same
# takes the entire dataset in input
# return a list of tuples (number of the frame, character)
def get_uniforme_frames(dataset):
    uniforme_frames = []
    for idx, frame in enumerate(dataset):
        if len(np.unique(frame['chars'])) == 1:
            uniforme_frames.append((idx, frame['chars'][0][0]))

    return uniforme_frames

# the dataset contains objects with one single occurrence
# discovered from the df
# remove the frames with these objects
def get_one_occurrences(dataset, df):
    one_occ_df = df[df['frequency'] == 1]
    one_occ_frames = []

    for idx, frame in tqdm(enumerate(dataset)):
        for value in zip(frame['chars'].flatten(), frame['colors'].flatten()):
            if value in list(zip(one_occ_df['char'], one_occ_df['color'])):
                one_occ_frames.append(idx)

    return one_occ_frames

# remove all the "void" around the minihack envs
# the function works on a single frame
# then map it on the entire dataset
def crop(frame):
    zero_rows =[]
    zero_cols =[]

    # get the indices of rows and columns with void chars
    # then remove those rows/cols from 'chars' and 'colors'
    for idx, row in enumerate(frame['chars']):
        if np.all(row == 32):
            zero_rows.append(idx)
    for idx, col in enumerate(frame['chars'].T):
        if np.all(col == 32):
            zero_cols.append(idx)

    # remove zero rows from chars and colors
    frame['chars'] = np.delete(frame['chars'], zero_rows, axis=0)
    frame['colors'] = np.delete(frame['colors'], zero_rows, axis=0)

    # remove zero cols from chars and colors
    frame['chars'] = np.delete(frame['chars'], zero_cols, axis=1)
    frame['colors'] = np.delete(frame['colors'], zero_cols, axis=1)

    return frame

# pad all frames to the same dimension, after cropping
def pad(dataset):
    # get the maximum frame dimension
    max_n_rows = 0
    max_n_cols = 0
    for frame in dataset:
        chars = frame['chars']
        n_rows, n_cols = chars.shape
        if n_rows > max_n_rows: max_n_rows = n_rows
        if n_cols > max_n_cols: max_n_cols = n_cols

    for frame in dataset:
        row_pad = max_n_rows - frame['chars'].shape[0]
        col_pad = max_n_cols - frame['chars'].shape[1]

        # pad "centering the frame" with blank spaces
        frame['chars'] = np.pad(frame['chars'],
            ((row_pad//2, row_pad//2 + row_pad%2),
             (col_pad//2, col_pad//2 + col_pad%2)),
             mode='constant', constant_values=ord(' '))

        frame['colors'] = np.pad(frame['colors'],
            ((row_pad//2, row_pad//2 + row_pad%2),
             (col_pad//2, col_pad//2 + col_pad%2)),
             mode='constant', constant_values=ord(' '))

def add_unique_id(dataset, mapper):
    for frame in dataset:
        frame['id'] = np.empty(frame['chars'].size)
        for idx, value in enumerate(zip(frame['chars'].flatten(), frame['colors'].flatten())):
            row = idx % frame['chars'].shape[0]
            col = idx // frame['chars'].shape[1]
            #frame['id'][row][col] = mapper[value] 
            frame['id'][idx] = mapper[value]
        frame['id'] = frame['id'].reshape(frame['chars'].shape)

def split(dataset, random_state):
    #stratifier = []
    #for f in dataset: stratifier.extend(list(f['id'].flatten()))
    training_set, test_set = tts(dataset, test_size=0.2, random_state=random_state)
    training_set, validation_set = tts(training_set, test_size=0.25, random_state=random_state) # 0.8*0.25 = 0.2

    return training_set, validation_set, test_set


def main():
    with open('../dataset/uncleaned_dataset.pkl', 'rb') as f: dataset = pickle.load(f)
    uniforme_frames = get_uniforme_frames(dataset)
    idxs = list(zip(*uniforme_frames))[0]

    print('Removing uniform frames')
    # remove "uniform" frames, i.e. frames with all 0s
    len_total = len(dataset)
    print(f'Number of frames before cleaning: {len(dataset)}')
    for idx in sorted(idxs, reverse=True): dataset.pop(idx)
    print(f'Number of frames after cleaning: {len(dataset)}')
    assert len_total == len(dataset) + len(uniforme_frames)

    # crop frames, i.e. remove rows/cols with zeros
    print('Cropping')
    dataset = list(map(crop, dataset))

    # pad all frames to the same dimensions
    print('Padding')
    pad(dataset)

    # remove frames with objects with one occurrence
    print('Removing frames with one-occurrences objects')
    df = pandas.read_pickle('../dataset/dataset.df')
    one_occ_frames = get_one_occurrences(dataset, df)
    for idx in sorted(one_occ_frames, reverse=True): dataset.pop(idx)

    with open('../dataset/dataset.pkl', 'wb') as f: pickle.dump(dataset, f)

    # add a unique id for each {char + color} combination
    # using the created mapper from Pytorch MiniHackDataset
    #with open('../dataset/dataset.mapper', 'rb') as f: mapper = pickle.load(f)
    #add_unique_id(dataset, mapper)

    print('Splitting and saving')
    tr_set, val_set, test_set = split(dataset, random_state=1)
    with open('../dataset/dataset.training.pkl', 'wb') as f: pickle.dump(tr_set, f)
    with open('../dataset/dataset.validation.pkl', 'wb') as f: pickle.dump(val_set, f)
    with open('../dataset/dataset.test.pkl', 'wb') as f: pickle.dump(test_set, f)


if __name__ == '__main__': main()