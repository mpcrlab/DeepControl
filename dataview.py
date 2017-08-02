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

data_files = []

for (dirpath, dirnames, filenames) in walk('/home/mpcr/Desktop/rodrigo/deepcontrol/dataset'):
    data_files.extend(filenames)
    break

h5f = []

for i in range(len(data_files)):
    h5f.append(h5py.File('/home/mpcr/Desktop/rodrigo/deepcontrol/dataset/' + data_files[i]))

for i in range(len(h5f)):
    image_set = np.asarray(h5f[i]['X'])
    action_array_set = np.asarray(h5f[i]['Y'])
    action_array_set = action_array_set.astype(int)
    mph = np.asarray(h5f[i]['Z'])
    mph = mph.astype(int)


nframes = action_array_set.shape[0]

fig = plt.figure()
ax = fig.add_subplot(111)
plt.ion()

fig.show()
fig.canvas.draw()

image_set = np.squeeze(image_set)

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

for i in range(nframes):
    ax.clear()
    ax.imshow(image_set[i,:,:])
    key_string = return_keys(action_array_set[i])
    print(key_string)
    fig.canvas.draw()
