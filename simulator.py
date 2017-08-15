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

class Pointer(object):
    def __init__(self,pointer_im,x=250,y=250):
        self.x = x
        self.y = y
        self.pointer_im = pointer_im
        self.pointer_im_rect = self.pointer_im.get_rect()
    def rotate(self, angle):
        rot_pointer_im = pygame.transform.rotate(self.pointer_im, angle)
        rot_pointer_rect = rot_pointer_im.get_rect()
        rot_pointer_rect.center = (self.pointer_im_rect.center[0]+self.x, self.pointer_im_rect.center[0]+self.y)

        return rot_pointer_im, rot_pointer_rect

pointer1 = Pointer(pygame.image.load("pointer.png").convert_alpha(), 200, 200)

dial1 = pygame.image.load("dial.gif").convert_alpha()

angle = 0
angle_minmax = (-45,135)
keystates={'up':False, 'down':False}
done = False

while not done:
    for event in pygame.event.get():
        keystates = get_keys(keystates)
        if event.type == pygame.QUIT:
            done = True
    if keystates['up'] and not angle > angle_minmax[1]:
        angle += 10
        print(angle)
    if keystates['down'] and not angle < angle_minmax[0]:
        angle -= 10
        print(angle)

    # Rotating image
    rot_pointer_im, rot_pointer_rect = pointer1.rotate(angle)

    # Blit rotated image
    screen.fill(WHITE)
    screen.blit(dial1, (pointer1.x-50,pointer1.y-50))
    screen.blit(rot_pointer_im, rot_pointer_rect)
    pygame.display.flip()
    clock.tick(20)

pygame.quit()
sys.exit()
