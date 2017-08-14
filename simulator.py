import sys
import pygame

def get_keys(keystates):
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_UP:
            keystates['up']=True
        if event.key == pygame.K_DOWN:
            keystates['down']=True
    #check for key up events
    if event.type == pygame.KEYUP:
        if event.key == pygame.K_UP:
            keystates['up']=False
        if event.key == pygame.K_DOWN:
            keystates['down']=False
    return keystates

BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)

# Initialize PyGame
pygame.init()
size = [500, 500]
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Spinning Dial")
clock = pygame.time.Clock()

# There's:
# pointer_im: loaded image
# pointer_im_rect: rectangle of loaded image
# rot_pointer_im: raw rotated image
# rot_pointer_rect: rectangle where the raw rotated image has to fit to

pointer_im = []

pointer_im = pygame.image.load("pointer.png").convert_alpha()
pointer_im_rect = pointer_im.get_rect()
x_pointer,y_pointer = (250,250)


angle = 0
angle_minmax = (0,90)
keystates={'up':False, 'down':False}
done = False

while not done:
    for event in pygame.event.get():
        keystates = get_keys(keystates)
        if event.type == pygame.QUIT:
            done = True
    if keystates['up'] and angle != angle_minmax[1]:
        angle += 10
        print(angle)
    if keystates['down'] and angle != angle_minmax[0]:
        angle -= 10
        print(angle)

    # Rotating image
    rot_pointer_im = pygame.transform.rotate(pointer_im, angle)
    rot_pointer_rect = rot_pointer_im.get_rect()
    rot_pointer_rect.center = pointer_im_rect.center

    # Blit rotated image
    screen.fill(WHITE)
    screen.blit(rot_pointer_im, rot_pointer_rect)
    pygame.display.flip()
    clock.tick(20)

pygame.quit()
sys.exit()
