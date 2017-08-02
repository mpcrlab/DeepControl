import numpy as np
import h5py
import tflearn
import matplotlib.pyplot as plt
import scipy.misc
import math
import matplotlib.cbook as cbook
from scipy.misc import imshow
import time


h5f = h5py.File('/home/mpcr/Desktop/rodrigo/deepcontrol/dataset/dataset.h5', 'r')

X = np.asarray(h5f['X'])
Y1 = np.asarray(h5f['Y'])
Y1 = Y1.astype(int)
Z = np.asarray(h5f['Z'])
Z = Z.astype(int)


nframes=Y1.shape[0]

fig = plt.figure()
ax = fig.add_subplot(111)
plt.ion()

fig.show()
fig.canvas.draw()

X = np.squeeze(X)

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
    ax.imshow(X[i,:,:])
    key_string = return_keys(Y1[i])
    #print(key_string)
    print(Z[i])
    fig.canvas.draw()
    #time.sleep(0.2)
