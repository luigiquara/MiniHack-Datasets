import pickle
import numpy as np
import pandas

# detect the uniform frames, i.e. where all characters are the same
# takes the entire dataset in input
# return a list of tuples (number of the frame, character)
def get_uniforme_frames(dataset):
    uniforme_frames = []
    for idx, frame in enumerate(dataset):
        if len(np.unique(frame['chars'])) == 1:
            uniforme_frames.append((idx, frame['chars'][0][0]))

    return uniforme_frames

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


with open('../uncleaned_dataset.pkl', 'rb') as f: dataset = pickle.load(f)
uniforme_frames = get_uniforme_frames(dataset)
idxs = list(zip(*uniforme_frames))[0]

'''
# remove "uniform" frames, i.e. frames with all 0s
len_total = len(dataset)
print(f'Number of frames before cleaning: {len(dataset)}')
for idx in sorted(idxs, reverse=True): dataset.pop(idx)
print(f'Number of frames after cleaning: {len(dataset)}')
assert len_total == len(dataset) + len(uniforme_frames)

new_dataset = list(map(crop, dataset))
with open('../dataset.pkl', 'wb') as f: pickle.dump(new_dataset, f)
'''