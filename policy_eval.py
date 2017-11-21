from __future__ import print_function
from Data import *
import os,sys
from network_run import *
from controlfunctions import *

import cv2
import pygame
import pygame.camera
from pygame.locals import *
from Pygame_UI import *
import pyrealsense as pyrs
from skimage import color
from skimage.transform import *
from Arduino import Arduino
import numpy as np
import time, datetime
import logging
import math, random
import numpy as np
import h5py
import tflearn
import matplotlib.pyplot as plt
import scipy.misc
from tflearn.layers.core import input_data, dropout, fully_connected
from tflearn.layers.conv import conv_2d, max_pool_2d
from tflearn.layers.normalization import local_response_normalization
from tflearn.layers.estimator import regression
import tensorflow as tf
tf.reset_default_graph()

class RoverRun():
	def __init__(self, framestack=False, film=False):
		self.d = Data()
		#self.userInterface = Pygame_UI()
		self.clock = pygame.time.Clock()
		self.FPS = 30
		self.image = None
		self.done = False
		self.paused = False
		self.angle = 0
		self.timeStart = time.time()
		self.stack = framestack
		self.film = film
		self.keystates = {'up':False, 'down':False, 'left':False, 'right':False, 'shift':False, 'space':False, 'enter':False}
		self.combo_dict = {
		0 : {'up':False, 'down':False, 'left':False, 'right':False, 'shift':False, 'space':False, 'enter':False},
		1 : {'up':True, 'down':False, 'left':False, 'right':False, 'shift':False, 'space':False, 'enter':False},
		2 : {'up':False, 'down':True, 'left':False, 'right':False, 'shift':False, 'space':False, 'enter':False},
		3 : {'up':False, 'down':False, 'left':True, 'right':False, 'shift':False, 'space':False, 'enter':False},
		4 : {'up':False, 'down':False, 'left':False, 'right':True, 'shift':False, 'space':False, 'enter':False},
		5 : {'up':False, 'down':False, 'left':False, 'right':False, 'shift':True, 'space':False, 'enter':False},
		6 : {'up':True, 'down':False, 'left':False, 'right':False, 'shift':True, 'space':False, 'enter':False},
		7 : {'up':False, 'down':True, 'left':False, 'right':False, 'shift':True, 'space':False, 'enter':False},
		8 : {'up':False, 'down':False, 'left':True, 'right':False, 'shift':True, 'space':False, 'enter':False},
		9 : {'up':False, 'down':False, 'left':False, 'right':True, 'shift':True, 'space':False, 'enter':False},
		10 : {'up':True, 'down':False, 'left':True, 'right':False, 'shift':False, 'space':False, 'enter':False},
		11 : {'up':True, 'down':False, 'left':False, 'right':True, 'shift':False, 'space':False, 'enter':False},
		12 : {'up':False, 'down':True, 'left':True, 'right':False, 'shift':False, 'space':False, 'enter':False},
		13 : {'up':False, 'down':True, 'left':False, 'right':True, 'shift':False, 'space':False, 'enter':False},
		14 : {'up':True, 'down':False, 'left':True, 'right':False, 'shift':True, 'space':False, 'enter':False},
		15 : {'up':False, 'down':True, 'left':True, 'right':False, 'shift':True, 'space':False, 'enter':False},
		16 : {'up':True, 'down':False, 'left':False, 'right':True, 'shift':True, 'space':False, 'enter':False},
		17 : {'up':False, 'down':True, 'left':False, 'right':True, 'shift':True, 'space':False, 'enter':False},
		18 : {'up':True, 'down':True, 'left':False, 'right':True, 'shift':True, 'space':False, 'enter':False},
		19 : {'up':True, 'down':False, 'left':True, 'right':True, 'shift':True, 'space':False, 'enter':False},
		}


		print("BBBBBBBBBBBBBBBBBBBBBBBBB")

		#pyrs.start()

		#self.cam = pyrs.Device(device_id = 0, streams = [pyrs.stream.ColorStream(fps = 30)])

		# Webcam (above is for Intel Realsense)
		cv2.namedWindow("preview")
		global vc
		vc = cv2.VideoCapture(0)

		print("CCCCCCCCCCCCCCCCCCCCCCCCCCCCCC")

		# Switch to root (sudo)
		print("Connecting to board...")
		#board = subprocess.check_output(['sudo', 'python', 'board_connect.py'])
		global board
		board = Arduino('9600')
		print("type: ", type(board))
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


		# Setup network prediction
		if framestack is False:
			self.network = input_data(shape=[None, 240, 320, 1])
			print("DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD")
		else:
			self.network = input_data(shape=[None, 240, 320, len(framestack)+1])
			self.framestack = np.zeros([1, 240, 320, self.FPS])
			self.stack.append(0)
			self.stack.sort()
		print("EEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE")
		self.network = Alex1(self.network)
		print("FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF")
		self.model = tflearn.DNN(self.network)
		print("GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG")
		self.model.load('/home/mpcr/Desktop/rodrigo/deepcontrol/saved_models/test6Alex1', weights_only=True)#/home/TF_Rover/RoverData/Felix_3frames10-20_FeatureScaling_DNN1',weights_only=True)
		print("HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH")
		self.run()

	def process_video_from_rover(self, jpegbytes, timestamp_10msec):
		array_of_bytes = np.fromstring(jpegbytes, np.uint8)
		self.image = cv2.imdecode(array_of_bytes, flags=3)
		k = cv2.waitKey(5) & 0xFF
		return self.image

	def onehot_to_combo(self, onehot):
		return self.combo_dict[onehot]


	def run(self):
		logging.basicConfig(filename='eval_logs/example.log',level=logging.DEBUG)
		hdlr = logging.FileHandler('/home/mpcr/Desktop/rodrigo/deepcontrol/eval_logs/example.log')
		formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
		hdlr.setFormatter(formatter)
		rval, frame = vc.read()
		cv2.imshow("preview", frame)
		key = cv2.waitKey(20)
		if key == 27: # Exit on ESCAPE
			sys.exit()
		c = np.mean(frame,2)#self.cam.color, 2)
		c = resize(c, (240,320))
		c = np.asarray(c)
		c = c[None, :, :, None]
		self.image = c

		while type(self.image) == type(None):
			print("self.image type None")
			time.sleep(10000000)

		while True:
			self.done = False
			# send "enter" key to arduino and wait for 2 seconds to reset get_name
			send_keys(board, {'right': False, 'space': False, 'shift': False, 'up': False, 'down': False, 'left': False, 'enter': True})
			time.sleep(2)
			start_time = time.time()
			while not self.done:
				rval, frame = vc.read()
				cv2.imshow("preview", frame)
				key = cv2.waitKey(20)
				if time.time()-start_time > 5:
					self.done = True
				if key == 27: # Exit on ESCAPE
					sys.exit()

				c = np.mean(frame,2)
				c = resize(c, (240,320))
				c = np.asarray(c)
				c = c[None, :, :, None]
				self.image = c

				current_frame = self.image

				# grayscale and crop
				# current_frame=np.mean(current_frame[None,110:,:,:], 3, keepdims=True)

				# Local Feature Scaling
				current_frame = (current_frame-np.mean(current_frame))/(np.std(current_frame)+1e-6)

				# Framestack
				if self.stack is not False:
					current = current_frame
					self.framestack = np.concatenate((current, self.framestack[:, :, :, 1:]), 3)
					current_frame = self.framestack[:, :, :, self.stack]

				# predict the correct steering angle from input
				self.angle = self.model.predict(current_frame)
				output_predictions = self.angle
				self.angle = np.argmax(self.angle)

				keystates = self.onehot_to_combo(self.angle)
				random_keystates = self.onehot_to_combo(random.randint(0,19))

				# print out feedback
				os.system('clear')
				print("Final prediction: " + str(self.angle), keystates)
				print("Predictions: " + str(output_predictions))
				print(self.image.shape)
				print(self.clock)


				# send predicted keystate to the arduino
				# send_keys(board, keystates)
				send_keys(board, {'right': False, 'space': False, 'shift': False, 'up': False, 'down': False, 'left': False, 'enter': True})
				self.clock.tick(self.FPS)

			elapsed_time = np.round(time.time() - start_time, 2)
			print('This run lasted %.2f seconds'%(elapsed_time))

			logging.info('date: {}: episode terminated after {}s'.format(datetime.datetime.now(), time.time()-start_time))

if __name__ == "__main__":
	print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
	rover = RoverRun()
