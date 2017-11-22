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

directory = '/home/mpcr/Desktop/rodrigo/deepcontrol/dataset'

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

fig = plt.figure()
ax = fig.add_subplot(111)
plt.ion()

fig.show()
fig.canvas.draw()

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
h5f = []
while True:
    x = raw_input("Type # of dataset to view: ")
    if x == "all":
        pass
    else:
        x = int(x)

    if not x in data_files:
        print(str(x) + " isn't in the datasets")
    else:
        h5f.append(h5py.File(directory + '/dataset' + str(data_files[x]) + '.h5'))

        image_set = np.asarray(h5f[0]['X'])
        image_set = image_set[:,:,:,None]
        image_set = np.squeeze(image_set)
        action_array_set = np.asarray(h5f[0]['Y'])
        action_array_set = action_array_set.astype(int)

        nframes = action_array_set.shape[0]
        for i in range(nframes-1):
            ax.clear()
            print("frame " + str(i) + " of %s" % nframes)
            print(image_set[i,:,:].shape)
            ax.imshow(image_set[i,:,:])
            key_string = return_keys(action_array_set[i])
            print(action_array_set)
            fig.canvas.draw()
            h5f = []
