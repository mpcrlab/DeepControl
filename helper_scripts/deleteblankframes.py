# controltrain1.py leaves some blank frames in every .h5 file,
# so this program deletes them

import numpy as np
import h5py
import tflearn
import matplotlib.pyplot as plt
import scipy.misc
import math
import matplotlib.cbook as cbook
from scipy.misc import imshow
import time
from os import walk
import sys

directory = '/home/mpcr/Desktop/rodrigo/deepcontrol/datasettemp'


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

if raw_input("Are you sure you want to continue? ") != "yes":
    sys.exit()

def return_keys(keystates):
    key_string = ""
    for i in range(len(keystates)):
        if keystates[i] == 1.:
            if i == 0:
                key_string += "right-"
            if i == 1:
                key_string += "down-"
            if i == 2:
                key_string += "shift-"
            if i == 3:
                key_string += "up-"
            if i == 4:
                key_string += "down-"
            if i == 5:
                key_string += "left-"
    return key_string

for set_num in range(len(data_files)):
    h5f = []
    print("Deleting blank frames from dataset %s" % data_files[set_num])
    h5f.append(h5py.File(directory + '/dataset' + str(data_files[set_num]) + '.h5'))

    image_set = np.asarray(h5f[0]['X'])
    action_array_set = np.asarray(h5f[0]['Y'])
    action_array_set = action_array_set.astype(int)
    mph = np.asarray(h5f[0]['Z'])
    mph = mph.astype(int)

    nframes = action_array_set.shape[0]


    image_set = np.squeeze(image_set)

    print(image_set.shape)

    for i in range(nframes-1):
        print("frame " + str(i) + " out of " + str(nframes))
        print("frame sum: %s" % np.sum(image_set[i,:,:]))
        if np.sum(image_set[i,:,:]) < 10:
            print(image_set.shape)
            image_set = np.delete(image_set, i, axis=0)
            print("Removed!, Shape: %s" % (str(image_set.shape)))
        key_string = return_keys(action_array_set[i])

    print(image_set.shape)
    print(action_array_set.shape)
    h5f = h5py.File(directory + '/fixed/dataset%s.h5' % data_files[set_num], 'w')
    h5f.create_dataset('X', data=image_set)
    h5f.create_dataset('Y', data=action_array_set)
    h5f.create_dataset('Z', data=mph)

    h5f.close()
