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
size = [750, 750]
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Spinning Dial")
clock = pygame.time.Clock()

class Pointer(object):
    def __init__(self,pointer_im,dial_im,x=250,y=250):
        self.x = x
        self.y = y
        self.angle = 135
        self.angle_minmax = (-45,135)
        self.dial_im = dial_im
        self.pointer_im = pointer_im
        self.pointer_im_rect = self.pointer_im.get_rect()
    def rotate(self, angle):
        rot_pointer_im = pygame.transform.rotate(self.pointer_im, angle)
        rot_pointer_rect = rot_pointer_im.get_rect()
        rot_pointer_rect.center = (self.pointer_im_rect.center[0]+self.x, self.pointer_im_rect.center[0]+self.y)

        return rot_pointer_im, rot_pointer_rect

class Slider(object):
    def __init__(self,rectangle_im,slider_im,x=500,y=250):
        self.x = x
        self.y = y
        self.rectangle_im = rectangle_im
        self.slider_im = slider_im
        self.value = 0
        self.value_minmax = (0,100)


pointer1 = Pointer(pygame.image.load("pointer.png").convert_alpha(),pygame.image.load("dial.gif").convert_alpha(), 200, 200)
slider1 = Slider(pygame.image.load("sliderrectangle1.png").convert_alpha(),pygame.image.load("bar.jpg").convert_alpha())

keystates={'up':False, 'down':False}
done = False

while not done:
    for event in pygame.event.get():
        keystates = get_keys(keystates)
        if event.type == pygame.QUIT:
            done = True
    if keystates['down'] and not slider1.value <= 0:
        slider1.value -= 5
        pointer1.angle = (-9 * slider1.value)/5 + 135
        print(slider1.value)
    if keystates['up'] and not slider1.value >= 100:
        slider1.value += 5
        pointer1.angle = (-9 * slider1.value)/5 + 135
        print(slider1.value)

    # Rotating image
    rot_pointer_im, rot_pointer_rect = pointer1.rotate(pointer1.angle)

    # Blit Dial
    screen.fill(WHITE)
    screen.blit(pointer1.dial_im, (pointer1.x-50,pointer1.y-50))
    screen.blit(rot_pointer_im, rot_pointer_rect)

    screen.blit(slider1.slider_im, (slider1.x, (slider1.y + 30) - slider1.value/3))
    screen.blit(slider1.rectangle_im, (slider1.x,slider1.y))
    pygame.display.flip()
    clock.tick(20)

pygame.quit()
sys.exit()
