import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image

##Rectangle parameters
rect = (175,25,375,50)
x0_mph = rect[0]
y0_mph = rect[1]
x1_mph = rect[2]
y1_mph = rect[3]
delta_x_mph = x1_mph-x0_mph
delta_y_mph = y1_mph-y0_mph


fig,ax = plt.subplots(1)

im = Image.open('mph.png')

ax.imshow(im)

rect = patches.Rectangle((x0_mph,y0_mph),delta_x_mph,delta_y_mph,linewidth=1,edgecolor='r',facecolor='none')

ax.add_patch(rect)

plt.show()

