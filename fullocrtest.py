import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import pyocr

from skimage import color
from PIL import Image, ImageFont, ImageDraw, ImageOps
import sys

import pyocr
import pyocr.builders
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
lang_time = langs[3]
print("Will use lang '%s' for time" % (lang_time))
# Ex: Will use lang 'fra'
# Note that languages are NOT sorted in any way. Please refer
# to the system locale settings for the default language
# to use.


def is_off_road(txt):
    if len(txt) > 10:
        return True
    else:
        return False


##Setting up crop parameters for "Time" window
#The resolution is 640x480
crop_time = (450,0,640,50)
x0_time = crop_time[0]
y0_time = crop_time[1]
x1_time = crop_time[2]
y1_time = crop_time[3]
delta_x_time = x1_time-x0_time
delta_y_time = y1_time-y0_time

##Setting up crop parameters for "MPH" window
crop_mph = (100,0,165,45)
x0_mph = crop_mph[0]
y0_mph = crop_mph[1]
x1_mph = crop_mph[2]
y1_mph = crop_mph[3]
delta_x_mph = x1_mph-x0_mph
delta_y_mph = y1_mph-y0_mph


##Initialize # of frames
frame_num = 100

##Initialize settings
a = raw_input("Enter 'road', 'time', or 'mph'")
if a == 'road':
    a = raw_input("Enter 'verbose' or 'road'")
    if a == 'verbose':
        b = 'road-verbose'
    else:
        b = 'road-road'
elif a == 'time':
    b = 'time'
elif a == 'mph':
    b = 'mph'
else:
    b = 'road-road'

##-------------------------------------------------------##
##                     Starting                          ##
##-------------------------------------------------------##

## start the service - also available as context manager
pyrs.start()

## create a device from device id and streams of interest
cam = pyrs.Device(device_id = 0, streams = [pyrs.stream.ColorStream(fps = 60)])
start = time.time()

## run input stream OCR
for _ in range(frame_num):
    cam.wait_for_frames()
    im = Image.fromarray(cam.color)
    grayscaled_im = Image.fromarray(color.rgb2gray(cam.color))
    cropped_time_im = im.crop(crop_time)
    cropped_mph_im = im.crop(crop_mph)
    if 'road' in b:
        txt_road = tool.image_to_string(
	        grayscaled_im,
            lang=lang_road,
            builder=pyocr.builders.TextBuilder())
        if b == 'road-verbose':
            print(txt_road)
        if b == 'road-road':
            if is_off_road(txt_road):
                print("OFFROAD")
                #Here, we will check for time passed
            else:
                print("ONROAD")
    if b == 'mph':
        txt_mph = tool.image_to_string(
            cropped_mph_im,
            lang=lang_time,
            builder=pyocr.builders.TextBuilder())
        print(txt_mph)
    elif b == 'time':
        txt_time = tool.image_to_string(
        cropped_time_im,
        lang=lang_time,
        builder=pyocr.builders.TextBuilder())
        print(txt_time)

##Print text crop rectangle

fig,ax = plt.subplots(1)

im = cam.color

ax.imshow(color.rgb2gray(cam.color))

rect_time = patches.Rectangle((x0_time,y0_time),delta_x_time,delta_y_time,linewidth=1,edgecolor='r',facecolor='none')

rect_mph = patches.Rectangle((x0_mph,y0_mph),delta_x_mph,delta_y_mph,linewidth=1,edgecolor='r',facecolor='none')

ax.add_patch(rect_time)
ax.add_patch(rect_mph)

#plt.imshow(cropped_mph_im, cmap='hot', interpolation='nearest')
plt.show()

## stop camera and service
cam.stop()
pyrs.stop()
elapsed = time.time()-start
fps = frame_num/elapsed

print("FPS: %s; Total time elapsed: %s" % (fps,elapsed,))
