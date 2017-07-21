import matplotlib.pyplot as plt
from PIL import Image
import numpy as np

## setup logging
import logging
logging.basicConfig(level = logging.INFO)

## import the package
import pyrealsense as pyrs

## start the service - also available as context manager
pyrs.start()

## create a device from device id and streams of interest
cam = pyrs.Device(device_id = 0, streams = [pyrs.stream.ColorStream(fps = 60)])

## retrieve 60 frames of data
for _ in range(20):
    cam.wait_for_frames()
    print(cam.color)
    a = cam.color

print("stopped")
## stop camera and service
cam.stop()
pyrs.stop()


plt.imshow(a, cmap='hot', interpolation='nearest')
a = Image.fromarray(a)
a.save('mph1.png')
plt.show()
