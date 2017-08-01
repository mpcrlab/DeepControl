import numpy as np
import h5py
import tflearn
import matplotlib.pyplot as plt
import scipy.misc
import math
import matplotlib.cbook as cbook
from scipy.misc import imshow


h5f = h5py.File('/home/mpcr/Desktop/rodrigo/deepcontrol/dataset/dataset.h5', 'r')

X = np.asarray(h5f['X'])
Y1 = np.asarray(h5f['Y'])
Y1 = Y1.astype(int)


Y=np.zeros((Y1.shape[0],np.max(Y1)+1))

for i in range(Y1.shape[0]):
	Y[i,Y1[i]]=1

nframes=Y1.shape[0]

fig = plt.figure()
ax = fig.add_subplot(111)
plt.ion()

fig.show()
fig.canvas.draw()

X = np.squeeze(X)

for i in range(nframes):
     print(i)
     print(Y1[i])
     ax.clear()
     ax.imshow(X[i,:,:])
     fig.canvas.draw()
