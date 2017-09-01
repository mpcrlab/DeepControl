from __future__ import print_function
import cv2
import pygame
from Data import *
import pygame.camera
from pygame.locals import *
from network_run import *
from Pygame_UI import *
from controlfunctions import *
import pyrealsense as pyrs
from skimage import color
from skimage.transform import *
import numpy as np
import time
import math
import numpy as np
import h5py
import tflearn
import matplotlib.pyplot as plt
import scipy.misc
import math
from tflearn.layers.core import input_data, dropout, fully_connected
from tflearn.layers.conv import conv_2d, max_pool_2d
from tflearn.layers.normalization import local_response_normalization
from tflearn.layers.estimator import regression
import tensorflow as tf
tf.reset_default_graph()
import os

class RoverRun():
    def __init__(self, framestack=False, film=False):
        self.d = Data()
        self.userInterface = Pygame_UI()
        self.clock = pygame.time.Clock()
        self.FPS = 30
        self.image = None
        self.quit = False
        self.paused = False
        self.angle = 0
        self.timeStart = time.time()
        self.stack = framestack
        self.film = film
        self.keystates = {'up':False, 'down':False, 'left':False, 'right':False, 'shift':False, 'space':False}
        print("BBBBBBBBBBBBBBBBBBBBBBBBB")

        #pyrs.start()

        #self.cam = pyrs.Device(device_id = 0, streams = [pyrs.stream.ColorStream(fps = 30)])

        ### ADDING THIS IN FOR webcam
        cv2.namedWindow("preview")
        global vc
        vc = cv2.VideoCapture(0)

        if self.film is True:
    	    pygame.camera.init()
            camlist = pygame.camera.list_cameras()
            print(camlist)
    	    if camlist:
    	        self.cam1 = pygame.camera.Camera(camlist[0],(640,480))
    	        self.cam1.start()

        print("CCCCCCCCCCCCCCCCCCCCCCCCCCCCCC")

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
        self.model.load('/home/mpcr/Desktop/rodrigo/deepcontrol/saved_models/dAlex1', weights_only=True)#/home/TF_Rover/RoverData/Felix_3frames10-20_FeatureScaling_DNN1',weights_only=True)
        print("HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH")
        self.run()

    def film_run(self):
        return pygame.surfarray.array3d(pygame.transform.rotate(self.cam.get_image(), 90))

    def process_video_from_rover(self, jpegbytes, timestamp_10msec):
        array_of_bytes = np.fromstring(jpegbytes, np.uint8)
        self.image = cv2.imdecode(array_of_bytes, flags=3)
        k = cv2.waitKey(5) & 0xFF
        return self.image



    def eraseFrames(self, count):
        size = len(self.d.angles)
        if (size - count > 0):
            print("--", "Deleting" , count, "seconds of frames!")
            self.d.angles = self.d.angles[:size - count]
            self.d.images = self.d.images[:size - count]
        else:
            print("Couldn't delete! List has less than", count, "frames!")


    def run(self):
        print("aoeu")
        start_time = time.time()
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

        print("aoeu")
        while not self.quit:
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

       	    key = get_keys(self.keystates)


    	    s=self.image

    	    if self.film is True:
    	        a = self.film_run()
    	        cv2.imshow('webcam', a)

    	    # grayscale and crop
            #s=np.mean(s[None,110:,:,:], 3, keepdims=True)

            # Local Feature Scaling
            s = (s-np.mean(s))/(np.std(s)+1e-6)

            # Framestack
            if self.stack is not False:
                current = s
                self.framestack = np.concatenate((current, self.framestack[:, :, :, 1:]), 3)
                s = self.framestack[:, :, :, self.stack]

    	    # predict the correct steering angle from input
            self.angle = self.model.predict(s)
            output_predictions = self.angle
            self.angle = np.argmax(self.angle)

            os.system('clear')
            print("Final prediction: " + str(self.angle))
            print("Predictions: " + str(output_predictions))
            print(self.image)
            print(self.image.shape)
            print(self.clock)

            cv2.imshow("RoverCam", scipy.misc.bytescale(np.mean(self.image, 2)))
    	    cv2.waitKey(1)

            self.clock.tick(self.FPS)
            pygame.display.flip()
            self.userInterface.screen.fill((255,255,255))

        elapsed_time = np.round(time.time() - start_time, 2)
        print('This run lasted %.2f seconds'%(elapsed_time))

        #self.set_wheel_treads(0,0)

        pygame.quit()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
    rover = RoverRun()
