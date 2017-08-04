from Arduino import Arduino
import pygame, sys
from pygame import mixer
import time
from controlfunctions import *
import io, os
from os import walk
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

# Creating "dataset" directory and cd-ing to it
print("Creating 'dataset' folder")
os.setuid(1000) #Changing permissions to user in order to create a folder that is non-root
if not os.path.exists('dataset'):
    os.makedirs('dataset')
print("'dataset' folder created")

# Detecting already saved data files and saving version numbers to a list
file_nums = []
for (dirpath, dirnames, filenames) in walk('/home/mpcr/Desktop/rodrigo/deepcontrol/dataset'):
    for i in range(len(filenames)):
        file_nums.append(int(filenames[i][7]))

# Function to determine which file number to use
def determine_batch_num(file_nums):
    last_contiguous = 0
    if len(file_nums) == 0:
        return 0
    if not file_nums[0] == 0:
        return 0
    for i in range(len(file_nums)):
        if file_nums[i] - last_contiguous == 1:
            last_contiguous += 1
        elif file_nums[i] - last_contiguous > 1:
            return last_contiguous + 1
    else:
        return file_nums[len(file_nums)-1] + 1

# Load audio countdown cue
mixer.init()
mixer.music.load('/home/mpcr/Desktop/rodrigo/deepcontrol/countdown.mp3')


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
        h5f.create_dataset('Z', data=self.mph)

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


##Initialize # of frames in a batch
frame_num = 500

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

current_frame = 0
current_batch = determine_batch_num(file_nums)

while True:
    while current_frame < frame_num:
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
            current_frame += 1

            if frame_num - current_frame == 80:
                mixer.music.play()
            if frame_num - current_frame == 1:
                mixer.music.load('/home/mpcr/Desktop/rodrigo/deepcontrol/beep-07.mp3')
                mixer.music.play()
        send_keys(board, keystates) #Send appropriate keystrokes from keystates through the arduino
        elapsed_frame = time.time()-frame_start
        print("Frame time: %s seconds" % elapsed_frame)
    if keystates == 'terminal':
        break
    # Perform this when batch collect is done
    print("Batch %s complete" % current_batch)
    # Wait for key command to save or not save
    while True:
        print("Press the 1 key (top of the keyboard) to save and continue on next batch...")
        print("Alternatively, press the 2 key to delete current batch and retry current batch")
        next_batch = False
        time.sleep(1)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    batch_start_time = time.time()
                    next_batch = True
                    d.save('/home/mpcr/Desktop/rodrigo/deepcontrol/dataset/dataset%s.h5' % current_batch)
                    file_nums.append(current_batch)
                    file_nums.sort()
                    print("TIME TOOK TO SAVE BATCH: %s" % (time.time()-batch_start_time))
                elif event.key == pygame.K_2:
                    next_batch = True
        if next_batch == True:
            break
    current_batch = determine_batch_num(file_nums)
    current_frame = 0
    is_collecting = False
    next_batch = False
    d.images = np.zeros((1,240,320,1))
    d.actions = np.zeros((1,6))
    d.mph = np.zeros((1))
    #mixer.music.load('/home/mpcr/Desktop/rodrigo/deepcontrol/countdown.mp3')
    print("Starting batch %s ..." % current_batch)

elapsed_total = time.time()-start
fps = frame_num/elapsed_total

print("FPS: %s; Total time elapsed: %s seconds" % (fps,elapsed_total))

##Print crop rectangles

fig,ax = plt.subplots(1)

ax.imshow(e)

rect_mph = patches.Rectangle((x0_mph,y0_mph),delta_x_mph,delta_y_mph,linewidth=1,edgecolor='r',facecolor='none')

ax.add_patch(rect_mph)

plt.show()

## stop camera and service
cam.stop()
pyrs.stop()
