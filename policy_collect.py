from Arduino import Arduino
import pygame, sys
from pygame import mixer
import time
from controlfunctions import *
import io, os
from os import walk
import h5py

import cv2
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

subject_id = raw_input("Please enter your first name and last initial here and press enter: ")

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

size = [560, 350]
WHITE = ( 255, 255, 255)
pygame.font.init()
myfont = pygame.font.SysFont('Comic Sans MS', 30)
textsurface = myfont.render('Some Text', False, (0, 0, 0))
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Click Here to Control")

pygame.key.set_repeat(50, 50)

print("Done initializing pygame")

keystates={'up':False, 'down':False, 'left':False, 'right':False, 'shift':False, 'space':False}

# Creating "dataset" directory and cd-ing to it
print("Creating 'dataset' folder")
os.setuid(1000) #Changing permissions to user in order to create a folder that is non-root
if not os.path.exists('/home/mpcr/Desktop/rodrigo/deepcontrol/study_dataset/' + subject_id):
    os.makedirs('/home/mpcr/Desktop/rodrigo/deepcontrol/study_dataset/' + subject_id)
print("'dataset' folder created")

# Detecting already saved data files and saving version numbers to a list
file_nums = []
for (dirpath, dirnames, filenames) in walk('/home/mpcr/Desktop/rodrigo/deepcontrol/study_dataset/' + subject_id):
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
mixer.music.load('/home/mpcr/Desktop/rodrigo/deepcontrol/beep-07.mp3')


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

##Initialize # of frames in a batch
frame_num = 500

##-------------------------------------------------------##
##                     Starting                          ##
##-------------------------------------------------------##
# Webcam setup
cv2.namedWindow("preview")
global vc
vc = cv2.VideoCapture(0)

rval, frame = vc.read()
cv2.imshow("preview", frame)
c = np.mean(frame,2)#self.cam.color, 2)
c = resize(c, (240,320))
c = np.asarray(c)
c = c[None, :, :, None]

start = time.time()

current_frame = 0
is_collecting = False

while True: # Ongoing infinite loop
    current_batch = determine_batch_num(file_nums)
    batch_frame = 0

    current_sub_batch = 0
    image_sub_batches = [np.zeros((1,240,320,1)) for i in range(6)]
    actions_sub_batches = [np.zeros((1,6)) for i in range(6)]

    d.images = np.zeros((1,240,320,1))
    d.actions = np.zeros((1,6))
    d.mph = np.zeros((1))
    os.system('clear')
    while batch_frame < frame_num: # Batch loop
        frame_start = time.time()
        current_frame += 1

        # Pygame UI
        screen.fill((255,255,255))
        text_to_screen(screen, "Current Batch: {}; Current frame: {}".format(str(current_batch), str(batch_frame)), 0, 50, 30, (0, 0, 0))

        keystates = get_keys(keystates) # Get keys that are currently pressed down, returns keystates dictionary

        #Get camera input stream
        rval, frame = vc.read()
        cv2.imshow("preview", frame)
        key = cv2.waitKey(20)
        if key == 27: # Exit on ESCAPE
            sys.exit()

        if keystates == 'terminal':
            break
        # Data collection on/off switch
        if keystates['space'] and not last_frame_space:
            # Turn data collection on/off
            mixer.music.play()
            is_collecting = not is_collecting
            if is_collecting:
                print("BEGINNING NEW 500 FRAME BATCH {}".format(current_batch))
            else:
                print("THREW AWAY BATCH {0}. PRESS SPACEBAR AGAIN TO RESTART BATCH {0}".format(current_batch))
                # print(image_sub_batches,current_sub_batch)
                current_sub_batch = 0
                image_sub_batches = [np.zeros((1,240,320,1)), np.zeros((1,240,320,1)), np.zeros((1,240,320,1)), np.zeros((1,240,320,1)), np.zeros((1,240,320,1)), np.zeros((1,240,320,1))]
                actions_sub_batches = [np.zeros((1,6)), np.zeros((1,6)), np.zeros((1,6)), np.zeros((1,6)), np.zeros((1,6)), np.zeros((1,6))]
                batch_frame = 0
        last_frame_space = keystates['space']

        # Manipulate keystates into a 0 and 1 array
        keystates_array = keystates.values() # Converts keystates into an array
        keystates_array = np.asarray(keystates_array) + 0.0 # Converts into Numpy array of 0's and 1's
        keystates_array = keystates_array[:,None] # Adds an extra dimension
        keystates_array = np.transpose(keystates_array) # Transposes array


        #Manipulate camera frame
        c = np.mean(frame,2)
        c = resize(c, (240,320))
        c = np.asarray(c)
        c = c[None, :, :, None]

        # Extract MPH from camera input stream
        im = Image.fromarray(frame)
        cropped_mph_im = im.crop(crop_mph)
        mph = np.full((1),curve_to_mph(cropped_mph_im, br_thresh))

        text_to_screen(screen, "Pressed keys: {}".format(keystates_array), 0, 90, 20, (0, 0, 0))

        if is_collecting:
            print("Frames collected for this batch: " + str(batch_frame))
            text_to_screen(screen, "Recording", 0, 0, 50, (200, 0, 0))

            if batch_frame % 100 == 0:
                current_sub_batch += 1

            image_sub_batches[current_sub_batch] = np.concatenate((image_sub_batches[current_sub_batch], c))
            actions_sub_batches[current_sub_batch] = np.concatenate((actions_sub_batches[current_sub_batch], keystates_array))
            d.mph = np.concatenate((d.mph, mph))
            batch_frame += 1
            if frame_num - batch_frame == 1:
                mixer.music.play()
        else:
            text_to_screen(screen, "Not Recording", 0, 0, 50, (0, 200, 0))

        pygame.display.flip()
        send_keys(board, keystates) #Send appropriate keystrokes from keystates through the arduino

        elapsed_frame = time.time()-frame_start
    if keystates == 'terminal':
        break
    # Perform this when batch collect is done
    print("Batch %s complete" % current_batch)

    # Finally concatenate image_sub_batches onto d.images
    for i in range(len(image_sub_batches)):
        d.images = np.concatenate((d.images, image_sub_batches[i]))
        d.actions = np.concatenate((d.actions, actions_sub_batches[i]))

    print("Saving to file...")
    batch_start_time = time.time()
    d.save('/home/mpcr/Desktop/rodrigo/deepcontrol/study_dataset/' + subject_id + '/dataset%s.h5' % current_batch)
    file_nums.append(current_batch)
    file_nums.sort()
