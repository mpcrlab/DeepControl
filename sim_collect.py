# Same as policy_collect.py EXCEPT this collects ONLY image frames. Adapted to nuclear reactor sim

import pygame, sys
import time, datetime
from controlfunctions import *
import io, os
from os import walk
import h5py

import cv2
from skimage import color
from skimage.transform import *
from imutils.perspective import four_point_transform
from imutils import contours
import imutils
from PIL import Image, ImageFont, ImageDraw, ImageOps, ImageStat
import matplotlib.pyplot as plt
import matplotlib.patches as patches

import pyocr
import pyocr.builders
import numpy as np

path = '/media/mpcr/Storage/deepcontrol/'
path = ''

subject_id = raw_input("Please enter your first name and last initial here and press enter: ")

print("Initializing pygame...")
pygame.init()

size = [560, 350]
pygame.font.init()
myfont = pygame.font.SysFont('Comic Sans MS', 30)
textsurface = myfont.render('Some Text', False, (0, 0, 0))
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Click Here to Control")
pygame.key.set_repeat(50, 50)

print("Done initializing pygame")

keystates={'decrease':False, 'increase':False, 'space':False}

# Creating "dataset" directory and cd-ing to it
print("Creating 'dataset' folder")
os.setuid(1000) #Changing permissions to user in order to create a folder that is non-root
if not os.path.exists(path + 'sim-datasets/' + subject_id):
	os.makedirs(path + 'sim-datasets/' + subject_id)
print("'dataset' folder created")

# Detecting already saved data files and saving version numbers to a list
file_nums = []
for (dirpath, dirnames, filenames) in walk(path + 'sim-datasets/' + subject_id):
	for i in range(len(filenames)):
		file_nums.append(int(filenames[i][7]))


#Setting up OCR
tools = pyocr.get_available_tools()
if len(tools) == 0:
	print("No OCR tool found")
	sys.exit(1)
# The tools are returned in the recommended order of usage
tool = tools[0]
print("Will use tool '%s'" % (tool.get_name()))

langs = tool.get_available_languages()
print("Available languages: %s" % ", ".join(langs))
lang = langs[langs.index('eng')]
print("Will use lang '%s'" % (lang))

br_thresh = 50

class Data():
	def __init__(self):
		self.actions = np.zeros((1,3))
		self.images = np.zeros((1,240,320,1))

	def load(self):
		pass

	def save(self, dset_name):
		self.images = np.asarray(self.images)
		self.actions = np.array(self.actions, dtype='float16')

		h5f = h5py.File(dset_name, 'w')
		h5f.create_dataset('X', data=self.images)
		h5f.create_dataset('Y', data=self.actions)

		h5f.close()

d = Data()

#The resolution is 640x480 (horizxvert)
##Setting up crop parameters for "MPH" window
crop_txt = (0,300,375,480)
x0_txt = crop_txt[0]
y0_txt = crop_txt[1]
x1_txt = crop_txt[2]
y1_txt = crop_txt[3]
delta_x_txt = x1_txt-x0_txt
delta_y_txt = y1_txt-y0_txt


## initialize data collection boolean variables
last_frame_space = False

##Initialize # of frames in a batch
frame_num = 500

##-------------------------------------------------------##
##                     Starting                          ##
##-------------------------------------------------------##
# Webcam setup
global vc
vc = cv2.VideoCapture(0)

rval, frame = vc.read()
c = np.mean(frame,2)
c = resize(c, (240,320))
c = np.asarray(c)
c = c[None, :, :, None]

start = time.time()

current_frame = 0
is_collecting = False

while True: # Ongoing infinite loop
	current_batch = str(datetime.datetime.now().replace(microsecond=0))
	current_batch = determine_batch_num(file_nums)
	batch_frame = 0

	current_sub_batch = 0
	image_sub_batches = [np.zeros((1,240,320,1)) for i in range(6)]
	actions_sub_batches = [np.zeros((1,3)) for i in range(6)]

	d.images = np.zeros((1,240,320,1))
	d.actions = np.zeros((1,3))
	os.system('clear')
	while batch_frame < frame_num: # Batch loop
		frame_start = time.time()
		current_frame += 1

		# Pygame UI
		screen.fill((255,255,255))
		text_to_screen(screen, "Current Batch: {}; Current frame: {}".format(current_batch, str(batch_frame)), 0, 50, 30, (0, 0, 0))

		keystates = get_keys(keystates) # returns keystates dictionary
		# special modification for this instance where you don't actually need keys
		# (automatic in nuclear reactor code)
		if keystates['space']:
			keystates = {'decrease':False, 'increase':False, 'space':True}
		else:
			keystates = {'decrease':False, 'increase':False, 'space':False}

		#Get camera input stream
		rval, frame = vc.read()
		raw = frame[:,:,:]
		cv2.rectangle(frame, (x0_txt, y0_txt), (x1_txt, y1_txt), (255,0,0), 2)
		cv2.imshow("raw", frame)
		cropped = raw[y0_txt:y1_txt, x0_txt:x1_txt]
		cv2.imshow("cropped", cropped)
		key = cv2.waitKey(20)
		if key == 27: # Exit on ESCAPE
			sys.exit()

		image = imutils.resize(image, height=500)
		gray = Image.fromarray(cv2.cvtColor(cropped, cv2.COLOR_BGR2GRAY))

		
		# fig,ax = plt.subplots(1)
		# ax.imshow(gray)

		# plt.show()

		txt = tool.image_to_string(
			Image.open('Figure_1.png'),
			lang=lang,
			builder=pyocr.builders.TextBuilder())
		txt = tool.image_to_string(
			gray,
			lang=lang,
			builder=pyocr.builders.DigitBuilder())
		print txt


		if keystates == 'terminal':
			break
		# Data collection on/off switch
		if keystates['space'] and not last_frame_space:
			# Turn data collection on/off
			is_collecting = not is_collecting
			if is_collecting:
				print("BEGINNING NEW 500 FRAME BATCH {}".format(current_batch))
			else:
				print("THREW AWAY BATCH {0}. PRESS SPACEBAR AGAIN TO RESTART BATCH {0}".format(current_batch))
				# print(image_sub_batches,current_sub_batch)
				current_sub_batch = 0
				image_sub_batches = [np.zeros((1,240,320,1)) for i in range(6)]
				actions_sub_batches = [np.zeros((1,3)) for i in range(6)]
				batch_frame = 0
		last_frame_space = keystates['space']

		# Manipulate keystates into a 0 and 1 array
		keystates_array = keystates.values() # Converts keystates into an array
		keystates_array = np.asarray(keystates_array) + 0.0 # Converts into NumPy array of 0's and 1's
		keystates_array = keystates_array[:,None] # Adds an extra dimension
		keystates_array = np.transpose(keystates_array)


		#Manipulate camera frame
		c = np.mean(frame,2)
		c = resize(c, (240,320))
		c = np.asarray(c)
		c = c[None, :, :, None]

		# Extract MPH from camera input stream
		im = Image.fromarray(frame)
		

		text_to_screen(screen, "Pressed keys: {}".format(keystates_array), 0, 90, 20, (0, 0, 0))
		text_to_screen(screen, '{}s'.format(str(round(time.time()-start, 2))), 0, 150, 50, (0, 0, 0))

		if is_collecting:
			print("Frames collected for this batch: " + str(batch_frame))
			text_to_screen(screen, "Recording", 0, 0, 50, (200, 0, 0))

			if batch_frame % 100 == 0:
				current_sub_batch += 1

			image_sub_batches[current_sub_batch] = np.concatenate((image_sub_batches[current_sub_batch], c))
			actions_sub_batches[current_sub_batch] = np.concatenate((actions_sub_batches[current_sub_batch], keystates_array))
			batch_frame += 1
		else:
			text_to_screen(screen, "Not Recording", 0, 0, 50, (0, 200, 0))

		pygame.display.flip()

		elapsed_frame = time.time()-frame_start
	if keystates == 'terminal':
		break
	# Perform this when batch collect is done
	print("Batch {} complete".format(current_batch))

	# Finally concatenate image_sub_batches onto d.images
	for i in range(len(image_sub_batches)):
		d.images = np.concatenate((d.images, image_sub_batches[i]))
		d.actions = np.concatenate((d.actions, actions_sub_batches[i]))

	print("Saving to file...")
	batch_start_time = time.time()
	d.save(path + 'sim-datasets/{}/dataset{}.h5'.format(subject_id, current_batch))
	file_nums.append(current_batch)
	file_nums.sort()
