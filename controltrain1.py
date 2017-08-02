from Arduino import Arduino
import pygame, sys
import time
from controlfunctions import *
import io, os
import h5py

from skimage import color
from skimage.transform import *
from PIL import Image, ImageFont, ImageDraw, ImageOps, ImageStat
import matplotlib.pyplot as plt
import matplotlib.patches as patches

import pyocr
import pyocr.builders
import pyrealsense as pyrs
import numpy as np

##################
# Initialization #
##################

print("Connecting to board...")
board = Arduino('9600')
print("Setting pin 13 to output...")
board.pinMode(13, "OUTPUT")

print("Setting pin 11 to output...")
board.pinMode(11, "OUTPUT")

print("Setting pin 9 to output...")
board.pinMode(9, "OUTPUT")

print("Setting pin 7 to output...")
board.pinMode(7, "OUTPUT")

print("Setting pin 5 to output...")
board.pinMode(5, "OUTPUT")

print("Setting pin 3 to output...")
board.pinMode(3, "OUTPUT")

print("Done configuring board")
time.sleep(1)
print("Initializing pygame...")
pygame.init()

size = [64, 48]
screen = pygame.display.set_mode(size)

pygame.key.set_repeat(50, 50)

print("Done initializing pygame")

keystates={'up':False, 'down':False, 'left':False, 'right':False, 'shift':False, 'space':False}

#Creating "dataset" directory and cd-ing to it
print("Creating 'dataset' folder")
os.setuid(1000) #Changing permissions to user in order to create a folder that is non-root
if not os.path.exists('dataset'):
    os.makedirs('dataset')
print("'dataset' folder created")


#Setting up OCR
tools = pyocr.get_available_tools()
if len(tools) == 0:
    print("No OCR tool found")
    sys.exit(1)
# The tools are returned in the recommended order of usage
tool = tools[0]
print("Will use tool '%s'" % (tool.get_name()))
# Ex: Will use tool 'libtesseract'

langs = tool.get_available_languages()
print("Available languages: %s" % ", ".join(langs))
lang_road = langs[5]
print("Will use lang '%s' for road" % (lang_road))

br_thresh = 50

class Data():
    def __init__(self):
        self.actions = np.zeros((1,6))
        self.images = np.zeros((1,240,320,1))
        self.mph = np.zeros((1))

    def load(self):
        pass

    def save(self, dset_name):

        self.images = np.asarray(self.images)

        self.actions = np.array(self.actions, dtype='float16')

        self.mph = np.array(self.mph, dtype='int')


        h5f = h5py.File(dset_name, 'w')
        h5f.create_dataset('X', data=self.images)
        h5f.create_dataset('Y', data=self.actions)

        h5f.close()

d = Data()

#The resolution is 640x480

##Setting up crop parameters for "MPH" window
crop_mph = (180,40,375,45)
x0_mph = crop_mph[0]
y0_mph = crop_mph[1]
x1_mph = crop_mph[2]
y1_mph = crop_mph[3]
delta_x_mph = x1_mph-x0_mph
delta_y_mph = y1_mph-y0_mph


## initialize data collection boolean variables
last_frame_space = False

is_collecting = False

terminal = False


##Initialize # of frames
frame_num = 100

##-------------------------------------------------------##
##                     Starting                          ##
##-------------------------------------------------------##
print("Starting pyrs...")
## start the service - also available as context manager
pyrs.start()
print("pyrs Started")

print("Creating device...")
## create a device from device id and streams of interest
cam = pyrs.Device(device_id = 0, streams = [pyrs.stream.ColorStream(fps = 60)])
print("Device created.")

start = time.time()

brightness_list = []

for _ in range(frame_num):#while True:
    frame_start = time.time()
    keystates = get_keys(keystates) # Get keys that are currently pressed down, returns keystates dictionary
    if keystates == 'terminal':
        break
    # Data collection on/off switch
    if keystates['space'] and not last_frame_space:
        # Turn data collection on/off
        is_collecting = not is_collecting
        if is_collecting:
            print("IS NOW COLLECTING DATA")
        else:
            print("STOPPED COLLECTING DATA")
    last_frame_space = keystates['space']

    keystates_array = keystates.values() # Converts keystates into an array
    keystates_array = np.asarray(keystates_array) + 0.0 # Converts into Numpy array of 0's and 1's
    keystates_array = keystates_array[:,None] # Adds an extra dimension
    keystates_array = np.transpose(keystates_array) # Transposes array

    cam.wait_for_frames() # This gets camera input stream as cam.color array
    # Create h5py file here, containing the numpy array and the array keystates_array
    #c = color.rgb2gray(cam.color)
    c = np.mean(cam.color, 2)
    e = c
    c = resize(c, (240,320))
    c = np.asarray(c)
    c = c[None, :, :, None]

    im = Image.fromarray(cam.color)
    cropped_mph_im = im.crop(crop_mph)
    mph = np.full((1),curve_to_mph(cropped_mph_im, br_thresh))


    if is_collecting:
        print("Is collecting...")
        d.images = np.concatenate((d.images, c))
        d.actions = np.concatenate((d.actions, keystates_array))
        d.mph = np.concatenate((d.mph, mph))


    send_keys(board, keystates) #Send appropriate keystrokes from keystates through the arduino
    elapsed_frame = time.time()-frame_start
    print("Elapsed time: %s seconds" % elapsed_frame)

d.save('/home/mpcr/Desktop/rodrigo/deepcontrol/dataset/dataset.h5')

elapsed = time.time()-start
fps = frame_num/elapsed

print("FPS: %s; Total time elapsed: %s seconds" % (fps,elapsed))

##Print crop rectangles

fig,ax = plt.subplots(1)

ax.imshow(e)

rect_mph = patches.Rectangle((x0_mph,y0_mph),delta_x_mph,delta_y_mph,linewidth=1,edgecolor='r',facecolor='none')

ax.add_patch(rect_mph)

plt.show()

## stop camera and service
cam.stop()
pyrs.stop()
