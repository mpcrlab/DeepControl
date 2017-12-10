# Converts NetLogo plot export CSV file (https://i.imgur.com/6zxeIpC.jpg) into labeled 
# actions the neural network can use to learn from as an .h5 file. The image frames are
# just placeholders for now.

import pandas as pd
import numpy as np
import h5py
from os import walk
import os

class Data():
	def __init__(self):
		self.actions = np.zeros((1,6))
		self.images = np.zeros((1,240,320,1))
		self.mph = np.zeros((1))

	def save(self, dset_name):
		self.images = np.asarray(self.images)
		self.actions = np.array(self.actions, dtype='float16')

		h5f = h5py.File(dset_name, 'w')
		h5f.create_dataset('X', data=self.images)
		h5f.create_dataset('Y', data=self.actions)
		h5f.create_dataset('Z', data=self.mph)

		h5f.close()

data = Data()

directory = '/media/mpcr/Storage/deepcontrol/sim-datasets'

if not os.path.isdir(directory + '/h5-dataset/'):
	os.makedirs(directory + '/h5-dataset/')


data_files = []

# Get all filenames of datasets into a list
for (dirpath, dirnames, filenames) in walk(directory):
	data_files.extend(filenames)
	break

print(data_files)

os.chdir(directory)

csv_file = pd.read_csv(data_files[0], sep='delimiter', header=None, error_bad_lines=False)

# parsing CSV file
i = 0
starts_at = 0
while True:
	try:
		if len(csv_file[0][i].split(',')) == 4 and csv_file[0][i].split(',')[3] == '"true"':
			print('starts at {}'.format(i))
			starts_at = i
			break
		else:
			i += 1
			continue
	except:
		i += 1
		continue

i = starts_at
csv_file = csv_file[0]
csv_array = []
while i < len(csv_file):
	item = [int(x[1:-1]) for x in csv_file[i].split(',')[1:-2]]
	csv_array.append(item)
	i += 1

i = 0
while i < len(csv_array)-1:
	if csv_array[i+1] > csv_array[i]:
		csv_array[i] = np.zeros((1,2))
		csv_array[i][0][1] = 1.
	elif csv_array[i+1] == csv_array[i]:
		csv_array[i] = np.zeros((1,2))
	elif csv_array[i+1] < csv_array[i]:
		csv_array[i] = np.zeros((1,2))
		csv_array[i][0][0] = 1.
	i += 1

del csv_array[-1] # this is because the last frame has nothing to compare to, so useless
data.actions = np.asarray(csv_array)
data.images = np.zeros((len(csv_array),240,320,1))

for i, thing in enumerate(data.actions):
	print(thing)

data.save(directory + '/h5-dataset/dataset100.h5')
