# This program takes data files and creates a log of a few randoom one-hot vector indices

from __future__ import division, print_function, absolute_import
import numpy as np
import h5py
import glob
import matplotlib.pyplot as plt
from random import randint
import sys
import os
from networkswitch import *
from sklearn.preprocessing import scale


# prompt the user to choose the name of the saved model
m_save = raw_input('What filename do you want to save this model as?')


# prompt the user for which model they want to train from networkswitch.py
print(modelswitch)
model_num = np.int32(raw_input('Which model do you want to train (0 - 11)?'))

# define useful variables
os.chdir('/home/mpcr/Desktop/rodrigo/deepcontrol/dataset')
fnames = glob.glob('*.h5') # datasets to train on
fnames.sort(key=lambda f: int(filter(str.isdigit, f)))
epochs = 50 # number of training iterations
batch_sz = 100  # training batch size
test_num = 650  # Number of validation examples
f_int = 5 # for framestack
f_int2 = 15 # for framestack
val_accuracy = [] # variable to store the validation accuracy
num_stack = 1
val_name = 'dataset31.h5' # Dataset to use for validation
num_iters = 0.
num_classes = 20
binary = False # Binary crossentropy or not
if binary:
    num_classes = 6

def batch_get(filename, batch_size):
    f = h5py.File(filename, 'r')
    X = np.asarray(f['X'])
    Y = np.int32(f['Y'])
    rand = np.random.randint(f_int2, X.shape[0], batch_sz)
    Y = Y[rand,:]
    f.flush()
    f.close()
    return Y

def combo_to_onehot(keystates_array):
    if keystates_array[1] == 1:
        keystates_array[1] = 0
    keystates_array = str(keystates_array)
    combo_dict = {
    '[0 0 0 0 0 0]' : 0,
    '[0 0 0 1 0 0]' : 1,
    '[0 0 0 0 1 0]' : 2,
    '[0 0 0 0 0 1]' : 3,
    '[1 0 0 0 0 0]' : 4,
    '[0 0 1 0 0 0]' : 5,
    '[0 0 1 1 0 0]' : 6,
    '[0 0 1 0 1 0]' : 7,
    '[0 0 1 0 0 1]' : 8,
    '[1 0 1 0 0 0]' : 9,
    '[0 0 0 1 0 1]' : 10,
    '[1 0 0 1 0 0]' : 11,
    '[0 0 0 0 1 1]' : 12,
    '[1 0 0 0 1 0]' : 13,
    '[0 0 1 1 0 1]' : 14,
    '[0 0 1 0 1 1]' : 15,
    '[1 0 1 1 0 0]' : 16,
    '[1 0 1 0 1 0]' : 17,
    '[1 0 1 1 1 0]' : 18,
    '[1 0 1 1 0 1]' : 19
    }
    one_hot = np.zeros((1,num_classes))
    i = combo_dict[keystates_array]
    one_hot[0][i] = 1
    return one_hot

def onehot_to_num(keystates_array):
    found = False
    index = 0
    while not found:
        if keystates_array[index] == 1:
            found = True
        else:
            index += 1
    return index

histogram = []
dataset_log = []

while True:
    #print(i)
    n = np.random.randint(0, len(fnames)-1, 1) # draw a random integer from 1 to # of files
    filename = fnames[n[0]] # name file according to the random number index

    print(len(dataset_log))

    if filename in dataset_log:
        print("I have already seen this dataset")
    else:
        if len(dataset_log) == 30:
            print("DONE")
            print(histogram)
        dataset_log.append(filename)

    # load the chosen data file
    Y = batch_get(filename, batch_sz)

    # Convert labels to one-hot vectors
    Z = np.zeros((batch_sz, num_classes))
    if binary == False:
        for i in range(len(Y)):
            Z[i] = combo_to_onehot(Y[i])
    Y = Z

    histogram.append(onehot_to_num(Y[randint(0,30)]))
