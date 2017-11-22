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

directory = '/home/mpcr/Desktop/rodrigo/deepcontrol/'

directory = directory + raw_input("Input folder path (from /deepcontrol): ")

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

for (dirpath, dirnames, filenames) in walk(directory):
    data_files.extend(filenames)
    break

for i in range(len(data_files)):
    if is_number(data_files[i][9]):
        data_files[i] = int(data_files[i][7] + data_files[i][8] + data_files[i][9])
    elif is_number(data_files[i][8]):
        data_files[i] = int(data_files[i][7] + data_files[i][8])
    else:
        data_files[i] = int(data_files[i][7])
data_files.sort()

print(data_files)

h5f = []

while True:
    x = raw_input("Type # of dataset to check framenum for: ")
    if x == "all":
        for i in range(len(data_files)):
            h5f.append(h5py.File(directory + '/dataset' + str(data_files[i]) + '.h5'))

            image_set = np.asarray(h5f[0]['X'])
            image_set = image_set[:,:,:,None]
            action_array_set = np.asarray(h5f[0]['Y'])
            action_array_set = action_array_set.astype(int)
            mph = np.asarray(h5f[0]['Z'])
            mph = mph.astype(int)

            action_frame_num = action_array_set.shape[0]
            image_frame_num = image_set.shape[0]
            if action_frame_num == image_frame_num:
                print("{}: Same!      Frame num: {}".format(str(i), action_frame_num))
            else:
                print("{}: Different! Action frame num: {}; Image frame num: {}".format(str(i), str(action_frame_num), str(image_frame_num)))
            h5f = []
        sys.exit()
    else:
        x = int(x)

    if not x in data_files:
        print(str(x) + " isn't in the datasets")
    else:
        h5f.append(h5py.File(directory + '/dataset' + str(data_files[x]) + '.h5'))


        image_set = np.asarray(h5f[0]['X'])
        image_set = image_set[:,:,:,None]
        action_array_set = np.asarray(h5f[0]['Y'])
        action_array_set = action_array_set.astype(int)
        mph = np.asarray(h5f[0]['Z'])
        mph = mph.astype(int)


        action_frame_num = action_array_set.shape[0]
        image_frame_num = image_set.shape[0]
        if action_frame_num == image_frame_num:
            print("Same!      Frame num: {}".format(action_frame_num))
        else:
            print("Different! Action frame num: {}; Image frame num: {}".format(str(action_frame_num), str(image_frame_num)))
        h5f = []
