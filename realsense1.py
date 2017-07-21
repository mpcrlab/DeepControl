import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import pyocr

from skimage import color
from PIL import Image, ImageFont, ImageDraw, ImageOps, ImageStat
import sys

import pyocr
import pyocr.builders
import numpy
import time
import pyrealsense as pyrs
import gym

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

def is_off_road(txt):
    if len(txt) > 10:
        return True
    else:
        return False

def dropoff(stat):
    for i in range(9):
        if np.abs(stat[-i-1]-stat[-i-2]) > br_thresh:
            return 10-i #Returns the rectangle right after the curve drops off
            break
    return 1

def curve_to_mph(im):
    width, height = im.size
    im_rects = []
    for i in range(10):    
        im_rects.append(im.crop((i*19,0,(i+1)*19,height)))
    stat = [ImageStat.Stat(im).mean[0] for im in im_rects]
    return dropoff(stat)


#The resolution is 640x480

##Setting up crop parameters for "MPH" window
crop_mph = (180,40,375,45)
x0_mph = crop_mph[0]
y0_mph = crop_mph[1]
x1_mph = crop_mph[2]
y1_mph = crop_mph[3]
delta_x_mph = x1_mph-x0_mph
delta_y_mph = y1_mph-y0_mph


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

## run input stream OCR
for _ in range(frame_num):
    done = False
    while True:
        ##Get camera input stream as im
        cam.wait_for_frames()
        im = Image.fromarray(cam.color)
        ##Post-processing
        grayscaled_im = Image.fromarray(color.rgb2gray(cam.color))

        ##Get "done"/episode termination due to lack of speed
        cropped_mph_im = im.crop(crop_mph)
        mph = curve_to_mph(cropped_mph_im)
        print(mph)
        if mph > 1:
            done_move = False
        else:
            done_move = True
        ##Get "done"/episode termination due to moving off of the road
        txt_road = tool.image_to_string(
	        grayscaled_im,
            lang=lang_road,
            builder=pyocr.builders.TextBuilder())
        done_road = is_off_road(txt_road)

        ##Get final "done"
        if done_road or done_move:
            done = True

        ##Get reward
        reward = 0
        ##Complete timestep information
        step_info = (im,reward,done)
        if done == True:
            print("Done Episode %s" % _)
            break


##Print crop rectangles

fig,ax = plt.subplots(1)

im = cam.color

ax.imshow(color.rgb2gray(cam.color))

rect_mph = patches.Rectangle((x0_mph,y0_mph),delta_x_mph,delta_y_mph,linewidth=1,edgecolor='r',facecolor='none')

ax.add_patch(rect_mph)

#plt.imshow(cropped_mph_im, cmap='hot', interpolation='nearest')
plt.show()

## stop camera and service
cam.stop()
pyrs.stop()
elapsed = time.time()-start
fps = frame_num/elapsed

print("FPS: %s; Total time elapsed: %s seconds" % (fps,elapsed))
