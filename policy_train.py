# author != michael teti

from __future__ import division, print_function, absolute_import
import numpy as np
import tensorflow as tf
import tflearn
from tflearn.layers.core import input_data, dropout, fully_connected
from tflearn.layers.conv import conv_2d, max_pool_2d
from tflearn.layers.normalization import local_response_normalization
from tflearn.layers.estimator import regression
from tflearn.helpers.trainer import Trainer
import h5py
from tflearn.metrics import *
from tflearn.objectives import categorical_crossentropy, binary_crossentropy
import glob
import matplotlib.pyplot as plt
from tflearn.data_augmentation import ImageAugmentation
import sys
import os
import cv2
from networkswitch import *
import operator
from random import randint
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
epochs = 5000 # number of training iterations
batch_sz = 200  # training batch size
test_num = 650  # Number of validation examples
f_int = 5 # for framestack
f_int2 = 15 # for framestack
val_accuracy = [] # variable to store the validation accuracy
num_stack = 1
val_name = 'dataset30.h5' # Dataset to use for validation
num_iters = 0.
num_classes = 20
binary = False # Binary crossentropy or not
if binary:
    num_classes = 6


def add_noise(x, y):
    x_aug = x + np.random.randn(x.shape[0], x.shape[1], x.shape[2], x.shape[3])
    x = np.concatenate((x, x_aug), 0)
    y = np.concatenate((y, y), 0)
    return x, y


def create_framestack(x, y, f_int, f_int2):
    X_ = []
    Y_ = []
    for ex_num in range(x.shape[0]-1, f_int2, -1):
        X2 = x[ex_num-f_int, :, :, :]
        X3 = x[ex_num-f_int2, :, :, :]
        X_.append(np.concatenate((x[ex_num, :, :, :], X2, X3), 2))
        Y_.append(y[ex_num, :])
    return np.asarray(X_), np.asarray(Y_)


def feature_scale(x):
    x = scale(x.reshape([x.shape[0], -1]), 1)
    return x.reshape([x.shape[0], 240, 320, 1])


def batch_get(filename, batch_size):
    f = h5py.File(filename, 'r')
    X = np.asarray(f['X'])
    Y = np.int32(f['Y'])
    #Y = np.zeros([batch_sz, num_classes])
    rand = np.random.randint(f_int2, X.shape[0], batch_sz)
    Y = Y[rand,:]
    X = X[rand,:,:]
    #Y[np.arange(batch_sz), y[rand]] = 1.0 # create one-hot label vector
    #X = np.mean(X[rand, 110:, :, :], 3, keepdims=True) # grayscale and crop frames
    #assert(X.shape[0] == Y.shape[0]), 'Data and labels different sizes'

    # Convert labels to one-hot vectors
    Z = np.zeros((batch_sz, num_classes))
    if binary == False:
        for j in range(len(Y)):
            Z[j] = combo_to_onehot(Y[j])
    Y = Z
    f.flush()
    f.close()
    return X, Y

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

# Validation set
print('Validation Dataset: %s'%(val_name))

# Create input layer and label placeholder for the network
labels = tf.placeholder(dtype=tf.float32, shape=[None, num_classes])
network = tf.placeholder(dtype=tf.float32, shape=[None, 240, 320, num_stack])


# send the input placeholder to the specified network
net_out = modelswitch[model_num](network)
acc = tf.reduce_mean(tf.to_float(tf.equal(tf.argmax(net_out, 1), tf.argmax(labels, 1))))
if binary:
    cost = binary_crossentropy(net_out, labels) # crossentropy loss function
else:
    cost = categorical_crossentropy(net_out, labels) # crossentropy loss function

# Tensorboard summaries
tf.summary.scalar('Accuracy_', acc)
tf.summary.scalar('Loss_', cost)
merged = tf.summary.merge_all()


# gradient descent optimizer
opt = tf.train.AdamOptimizer(learning_rate=0.000033)
trainop = tflearn.TrainOp(loss=cost,
                         optimizer=opt,
                         metric=None,
                         batch_size=batch_sz)
model = Trainer(train_ops=trainop)

writer = tf.summary.FileWriter('/tmp/tflearn_logs/test'+m_save+modelswitch[model_num].__name__,
                               model.session.graph)
writer2 = tf.summary.FileWriter('/tmp/tflearn_logs/train'+m_save+modelswitch[model_num].__name__,
                               model.session.graph)

out_log = []
i = -1

while i < epochs:
    i += 1
    print("Epoch: %s" % i)
    n = np.random.randint(0, len(fnames)-1, 1) # draw a random integer from 1 to # of files
    filename = fnames[n[0]] # name file according to the random number index
    # skip validation set if chosen
    if filename == val_name:
        continue

    # load the chosen data file
    X, Y = batch_get(filename, batch_sz)

    # local feature Scaling
    X = feature_scale(X)

    # framestack
    if num_stack != 1:
        X, Y = create_framestack(X, Y, f_int, f_int2)

    # Data Augmentation
    #X, Y = add_noise(X, Y)

    # Training
    model.fit_batch(feed_dicts={network:X, labels:Y})

    #Visualize output
    out = model.session.run(net_out, feed_dict={network:X, labels:Y})
    out_ = []
    for j in range(out.shape[1]):
        out_.append(out[0][j])
    out = out_
    out_log.append(out)

    train_acc, train_loss = model.session.run([acc, cost], feed_dict={network:X, labels:Y})

    train_summary = model.session.run(merged, feed_dict={network:X, labels:Y})
    writer2.add_summary(train_summary, i)

    if i%50 == 0:
        print("Validating")
        # get validation batch
        tx, ty = batch_get(val_name, 500)
        # feature scale validation data
        tx = feature_scale(tx)

        # Create validation framestack
        if num_stack != 1:
            tx, ty = create_framestack(tx, ty, f_int, f_int2)
        assert(ty.shape[0] == tx.shape[0]),'data and label shapes do not match'

        # Get validation accuracy and error rate
        val_acc, val_loss, summary = model.session.run([acc, cost, merged],
                                                   feed_dict={network:tx, labels:ty})
        writer.add_summary(summary, i)

# Save model and acc/error curves
os.chdir('/home/mpcr/Desktop/rodrigo/deepcontrol/saved_models')
model.save(m_save+modelswitch[model_num].__name__)

# Save model output throughout training
os.chdir('/home/mpcr/Desktop/rodrigo/deepcontrol/policy_output')
output_file = open(str(m_save+modelswitch[model_num].__name__) + '.txt', 'w')
output_file.write(str(out_log))
