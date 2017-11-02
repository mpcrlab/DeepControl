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

for i in range(len(data_files)):
    x = raw_input("Append %s? (Y/N): " % data_files[i])
    if x == "Y" or x == "y":
        h5f.append(h5py.File(directory + '/dataset' + str(data_files[i]) + '.h5'))
    elif x == "s":
        break
    else:
        pass


print(h5f[0]['X'].shape)
image_set = np.asarray(h5f[0]['X'])
image_set = image_set[:,:,:,None]
action_array_set = np.asarray(h5f[0]['Y'])
action_array_set = action_array_set.astype(int)
mph = np.asarray(h5f[0]['Z'])
mph = mph.astype(int)

print(image_set[0])

if len(h5f) > 1:
    for i in range(1,len(h5f)):
        print(np.asarray(h5f[i]['X'])[:,:,:,None].shape)
        print(image_set.shape)
        image_set = np.concatenate((image_set, np.asarray(h5f[i]['X'])[:,:,:,None]))
        action_array_set = np.concatenate((action_array_set, np.asarray(h5f[i]['Y'])))
        action_array_set = action_array_set.astype(int)
        mph = np.concatenate((mph, h5f[i]['Z']))
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
    #print("Type %s" % type(image_set[i,5,5]))
    ax.clear()
    print("frame " + str(i) + " of %s" % nframes)
    ax.imshow(image_set[i,:,:])
    key_string = return_keys(action_array_set[i])
    print(action_array_set)
    fig.canvas.draw()
