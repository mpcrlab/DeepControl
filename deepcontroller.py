import pygame, sys

## Configuring pygame.key.get_pressed() key codes
K_UP = 273
K_DOWN = 274
K_RIGHT = 275
K_LEFT = 276
K_LSHIFT = 304

def get_keys(keystates):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
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
    return keystates

def send_keys(board, keystates):
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
