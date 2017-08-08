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

for (dirpath, dirnames, filenames) in walk('/home/mpcr/Desktop/rodrigo/deepcontrol/dataset'):
    data_files.extend(filenames)
    break

for i in range(len(data_files)):
    if is_number(data_files[i][8]):
        data_files[i] = int(data_files[i][7] + data_files[i][8])
    else:
        data_files[i] = int(data_files[i][7])
data_files.sort()

print(data_files)

h5f = []

for i in range(len(data_files)):
    x = raw_input("Append %s? (Y/N): " % i)
    if x == "Y" or x == "y":
        h5f.append(h5py.File('/home/mpcr/Desktop/rodrigo/deepcontrol/dataset/dataset' + str(data_files[i]) + '.h5'))
    else:
        pass


image_set = np.asarray(h5f[0]['X'])
action_array_set = np.asarray(h5f[0]['Y'])
action_array_set = action_array_set.astype(int)
mph = np.asarray(h5f[0]['Z'])
mph = mph.astype(int)

if len(h5f) > 1:
    for i in range(1,len(h5f)):
        print(i)
        image_set = np.concatenate((image_set, np.asarray(h5f[i]['X'])))
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
print(image_set.shape)

for i in range(nframes):
    ax.clear()
    print(np.sum(image_set[i,:,:]))
    print("frame " + str(i))
    ax.imshow(image_set[i,:,:])
    if np.sum(image_set[i,:,:]) == 0.0:
        print(image_set.shape)
        image_set = np.delete(image_set, i, axis=0)
        print("Removed!, Shape: %s" % (str(image_set.shape)))
    key_string = return_keys(action_array_set[i])
    print(action_array_set)
    fig.canvas.draw()

print(image_set.shape)
print(action_array_set.shape)
h5f = h5py.File('/home/mpcr/Desktop/rodrigo/deepcontrol/dataset/noblanks0.h5', 'w')
h5f.create_dataset('X', data=image_set)
h5f.create_dataset('Y', data=action_array_set)
h5f.create_dataset('Z', data=mph)

h5f.close()

#103, 204, 305
#406, 507, 610, 711, 812, 913, 1014, 1015, 1016
