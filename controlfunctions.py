import pygame, sys
import numpy as np
from PIL import Image, ImageStat

## Configuring pygame.key.get_pressed() key codes
K_UP = 273
K_DOWN = 274
K_RIGHT = 275
K_LEFT = 276
K_LSHIFT = 304
K_SPACE = 32

def is_off_road(txt):
    if len(txt) > 10:
        return True
    else:
        return False

def dropoff(stat, br_thresh):
    for i in range(9):
        if np.abs(stat[-i-1]-stat[-i-2]) > br_thresh:
            return 10-i #Returns the rectangle right after the curve drops off
            break
    return 1

def curve_to_mph(im, br_thresh):
    width, height = im.size
    im_rects = []
    for i in range(10):
        im_rects.append(im.crop((i*19,0,(i+1)*19,height)))
    stat = [ImageStat.Stat(im).mean[0] for im in im_rects]
    return dropoff(stat, br_thresh)

def get_keys(keystates):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            return 'terminal'
        keys = pygame.key.get_pressed()
        #check for key down events
        if event.type == pygame.KEYDOWN:
            if event.key == K_UP:
                keystates['up']=True
            if event.key == K_DOWN:
                keystates['down']=True
            if event.key == K_LEFT:
                keystates['left']=True
            if event.key == K_RIGHT:
                keystates['right']=True
            if event.key == K_LSHIFT:
                keystates['shift']=True
            if event.key == K_SPACE:
                keystates['space']=True

        #check for key up events
        if event.type == pygame.KEYUP:
            if event.key == K_UP:
                keystates['up']=False
            if event.key == K_DOWN:
                keystates['down']=False
            if event.key == K_LEFT:
                keystates['left']=False
            if event.key == K_RIGHT:
                keystates['right']=False
            if event.key == K_LSHIFT:
                keystates['shift']=False
            if event.key == K_SPACE:
                keystates['space']=False
    return keystates

def send_keys(board, keystates):
    if isinstance(keystates, dict):
        #do something about the key states here, now that the event queue has been processed
        if keystates['up']:
            print("Up")
            board.digitalWrite(9, "HIGH")
        else:
            board.digitalWrite(9, "LOW")


        if keystates['down']:
            print("Down")
            board.digitalWrite(7, "HIGH")
        else:
            board.digitalWrite(7, "LOW")


        if keystates['left'] and keystates['shift']:
            print("Hard left")
            board.digitalWrite(3, "HIGH")
        else:
            board.digitalWrite(3, "LOW")


        if keystates['left'] and not keystates['shift']:
            print("Left")
            board.digitalWrite(5, "HIGH")
        else:
            board.digitalWrite(5, "LOW")


        if keystates['right'] and keystates['shift']:
            print("Hard right")
            board.digitalWrite(13, "HIGH")
        else:
            board.digitalWrite(13, "LOW")


        if keystates['right'] and not keystates['shift']:
            print("Right")
            board.digitalWrite(11, "HIGH")
        else:
            board.digitalWrite(11, "LOW")

        print("---------------------\n")

    else:
        #do something about the key states here, now that the event queue has been processed
        if keystates[0][3]:
            print("Up")
            board.digitalWrite(9, "HIGH")
        else:
            board.digitalWrite(9, "LOW")


        if keystates[0][0]:
            print("Down")
            board.digitalWrite(7, "HIGH")
        else:
            board.digitalWrite(7, "LOW")


        if keystates[0][4] and keystates[0][1]:
            print("Hard left")
            board.digitalWrite(3, "HIGH")
        else:
            board.digitalWrite(3, "LOW")


        if keystates[0][4] and not keystates[0][1]:
            print("Left")
            board.digitalWrite(5, "HIGH")
        else:
            board.digitalWrite(5, "LOW")


        if keystates[0][2] and keystates[0][1]:
            print("Hard right")
            board.digitalWrite(13, "HIGH")
        else:
            board.digitalWrite(13, "LOW")


        if keystates[0][2] and not keystates[0][1]:
            print("Right")
            board.digitalWrite(11, "HIGH")
        else:
            board.digitalWrite(11, "LOW")

        print("---------------------\n")
