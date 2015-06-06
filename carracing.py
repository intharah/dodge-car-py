# INTIALISATION
import pygame, math, sys
from pygame.locals import *
from pyscope import pyscope

width = 640
height = 480

if (sys.platform == "darwin"):
    screen = pygame.display.set_mode((width, height))
else:
    scope = pyscope()
    screen = scope.screen
    width = screen.get_size()[0]
    height = screen.get_size()[1]
clock = pygame.time.Clock()
background = pygame.Surface(screen.get_size())
print screen.get_size()[0]
background = background.convert()
background.fill((250, 250, 250))
background_img = pygame.image.load("grass.png").convert()
crash = False

# This is a list of 'sprites.' Each block in the program is
# added to this list.
# The list is managed by a class called 'Group.'
block_list = pygame.sprite.Group()
 
# This is a list of every sprite.
# All blocks and the player block as well.
all_sprites_list = pygame.sprite.Group()


class PadSprite(pygame.sprite.Sprite):
    normal = pygame.image.load("car.png")
    hit = pygame.image.load("pad_hit.png")
    def __init__(self,number,position):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)
        # Load the image
        self.image = self.normal
        self.number = number
        self.position = position
        self.rect = self.image.get_rect()
        self.rect.center = self.position
    def update(self, hit_list):
        if self in hit_list: self.image = self.hit
        else: self.image = self.normal
    
class CarSprite(pygame.sprite.Sprite):
    MAX_FORWARD_SPEED = 10
    MAX_REVERSE_SPEED = 10
    ACCELERATION = 2
    TURN_SPEED = 5
    car_hit = pygame.image.load("pad_hit.png")
    car_img = pygame.image.load("car.png")
    def __init__(self, position):
        pygame.sprite.Sprite.__init__(self)
        self.src_image = self.car_img
        self.position = position
        self.rect = self.car_img.get_rect()
        self.speed = self.direction = 0
        self.k_left = self.k_right = self.k_down = self.k_up = 0
    def update(self, deltat):
        # SIMULATION
        self.speed += (self.k_up + self.k_down)
        if self.speed > self.MAX_FORWARD_SPEED:
            self.speed = self.MAX_FORWARD_SPEED
        if self.speed < -self.MAX_REVERSE_SPEED:
            self.speed = -self.MAX_REVERSE_SPEED
        self.direction += (self.k_right + self.k_left)
        x, y = self.position
        rad = self.direction * math.pi / 180
        x += -self.speed*math.sin(rad)
        y += -self.speed*math.cos(rad)
        self.position = (x, y)
        self.image = pygame.transform.rotate(self.src_image, self.direction)
        self.rect = self.image.get_rect()
        self.rect.center = self.position
            
# CREATE A CAR AND RUN
rect = screen.get_rect()
car = CarSprite(rect.center)
car_group = pygame.sprite.RenderPlain(car)

all_sprites_list.add(car_group)

# CREATE PADS
pads = [
    PadSprite(1,(100, 100)),
    PadSprite(2,(300, 100))
]
pad_group = pygame.sprite.RenderPlain(*pads)
all_sprites_list.add(*pads)


pygame.font.init()
basicfont = pygame.font.Font('data/coders_crux/coders_crux.ttf', 20)


while 1:
    # USER INPUT
    deltat = clock.tick(30)
    for event in pygame.event.get():
        if not hasattr(event, 'key'): continue
        down = event.type == KEYDOWN
        if crash == False:
            if event.key == K_RIGHT: car.k_right = down * -5
            elif event.key == K_LEFT: car.k_left = down * 5
            elif event.key == K_UP: car.k_up = down * 2
            elif event.key == K_DOWN: car.k_down = down * -2
            elif event.key == K_SPACE: car.k_space = down * 0
        if event.key == K_ESCAPE: pygame.quit()
    # RENDERING
    screen.blit(background_img,(0,0))
    pad_group.clear(screen, background)
    car_group.clear(screen, background)
    
    # display fps
    text = basicfont.render("%d fps" % int(clock.get_fps()), True, (255, 0, 0), (255, 255, 255))
    textrect = text.get_rect()
    textrect.centerx = text.get_rect().width /2
    textrect.centery = 10
    screen.fill((255, 255, 255))
    screen.blit(text, textrect)

    car_group.update(deltat)
    # CHECK IF CAR IS LEAVING SCREEN
    if car.rect.right>width:
        car.rect.right = width
    elif car.rect.left<0:
        car.rect.left = 0
    elif car.rect.bottom>height:
        car.rect.bottom = height
    elif car.rect.top<0:
        car.rect.top = 0
    # DRAW ALL SPRITES
    all_sprites_list.draw(screen)
    pads = pygame.sprite.spritecollide(car, pad_group, False)
    if pads:
        car.src_image = car.car_hit
        car.speed = 0
        car.k_left = car.k_right = car.k_down = car.k_up = 0
        crash = True
    pygame.display.flip()
