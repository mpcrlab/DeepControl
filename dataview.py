import numpy as np
import h5py
import tflearn
import matplotlib.pyplot as plt
import scipy.misc
import math
import matplotlib.cbook as cbook
from scipy.misc import imshow


h5f = h5py.File('/home/mpcr/Desktop/rodrigo/deepcontrol/dataset/dataset.h5', 'r')


print(h5f.keys())



X = np.asarray(h5f['X'])
Y1 = np.asarray(h5f['Y'])
Y1 = Y1.astype(int)


print(X.shape)
print(Y1.shape)

print(Y1)

print(np.max(Y1)+1)

Y=np.zeros((Y1.shape[0],np.max(Y1)+1))

for i in range(Y1.shape[0]):
	Y[i,Y1[i]]=1

#print(Y)

nframes=Y1.shape[0]

fig = plt.figure()
ax = fig.add_subplot(111)
plt.ion()

fig.show()
fig.canvas.draw()

X = np.squeeze(X)
print(X.shape)
image_file = cbook.get_sample_data('grace_hopper.png')
image = plt.imread(image_file)

fig, ax = plt.subplots()
#im = ax.imshow(X[55,:,:])
print("oeurggd")
#ax.axis('off')
plt.show()

for i in range(nframes):
     print(i)
     print(Y1[i])
     ax.clear()
     ax.imshow(X[i,:,:])
     fig.canvas.draw()
