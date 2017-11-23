# controltrain1.py leaves float64 pixels, which increases RAM consumption,
# so this program converts every pixel to float16

import numpy as np
import h5py
import os
from os import walk

directory = '/home/mpcr/Desktop/rodrigo/deepcontrol/study_dataset/'

directory = directory + raw_input("Input folder name: ")

if not os.path.isdir(directory + '/fixed/'):
    os.makedirs(directory + '/fixed/')

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass
    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass
    return False

data_files = []

# Get all filenames of datasets into a list
for (dirpath, dirnames, filenames) in walk(directory):
    data_files.extend(filenames)
    break
# Extract the dataset numbers
for i in range(len(data_files)):
    if is_number(data_files[i][9]):
        data_files[i] = int(data_files[i][7] + data_files[i][8] + data_files[i][9])
    elif is_number(data_files[i][8]):
        data_files[i] = int(data_files[i][7] + data_files[i][8])
    else:
        data_files[i] = int(data_files[i][7])
data_files.sort()

print(data_files)

for set_num in range(len(data_files)):
    h5f = []
    print("Converting datatypes on dataset %s" % data_files[set_num])
    h5f.append(h5py.File(directory + '/dataset' + str(data_files[set_num]) + '.h5'))

    image_set = np.asarray(h5f[0]['X'])
    action_array_set = np.asarray(h5f[0]['Y'])
    action_array_set = action_array_set.astype(int)
    mph = np.asarray(h5f[0]['Z'])
    mph = mph.astype(int)

    image_set = np.squeeze(image_set)
    image_set = image_set.astype(np.uint8)
    h5f = h5py.File(directory + '/fixed/dataset%s.h5' % data_files[set_num], 'w')
    h5f.create_dataset('X', data=image_set)
    h5f.create_dataset('Y', data=action_array_set)
    h5f.create_dataset('Z', data=mph)

    h5f.close()
