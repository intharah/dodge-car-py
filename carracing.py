# INTIALISATION
import pygame, math, sys, subprocess
from pygame.locals import *
from pyscope import pyscope

width = 640
height = 480

lifeP1 = 100
lifeP2 = 100
lifeP3 = 100

time = 99
pygame.time.set_timer(USEREVENT+1, 1000)

if (sys.platform == "darwin") or (sys.platform == "win32"):
    screen = pygame.display.set_mode((width, height))
else:
    scope = pyscope()
    screen = scope.screen
    width = screen.get_size()[0]
    height = screen.get_size()[1]

clock = pygame.time.Clock()
background = pygame.Surface(screen.get_size())
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

class DisplayText:
    def __init__(self,message,font_type,color,posX,posY,marginX,marginY):
        self.msg = font_type.render(message, True, color)
        self.msgRect = self.msg.get_rect()
        self.msgRect.centerx = posX + marginX
        self.msgRect.centery = posY + marginY

    def render(self):
        screen.blit(self.msg, self.msgRect)

class PadSprite(pygame.sprite.Sprite):
    def __init__(self,number,position,normal):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)
        # Load the image
        self.image = normal
        self.number = number
        self.position = position
        self.rect = self.image.get_rect()
        self.rect.center = self.position
    def update(self, hit_list, hit):
        if self in hit_list: self.image = hit
        else: self.image = normal
    
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
        #print self.position
            
# CREATE A CAR AND RUN
rect = screen.get_rect()
car = CarSprite(rect.center)
car_group = pygame.sprite.RenderPlain(car)
all_sprites_list.add(car_group)

# CREATE PADS
pads = [
    PadSprite(1,(100, 100), pygame.image.load("car.png")),
    PadSprite(2,(300, 100), pygame.image.load("car.png"))
]
pad_group = pygame.sprite.RenderPlain(*pads)
all_sprites_list.add(*pads)

# CREATE BONUS
bonus = PadSprite(1,(150,200), pygame.image.load("bonus.png"))
bonus_group = pygame.sprite.RenderPlain(bonus)
all_sprites_list.add(bonus_group)

pygame.font.init()
basicfont = pygame.font.Font('data/coders_crux/coders_crux.ttf', 20)
mediumfont = pygame.font.Font('data/coders_crux/coders_crux.ttf', 40)
bigfont = pygame.font.Font('data/coders_crux/coders_crux.ttf', 70)


while 1:
    # USER INPUT
    deltat = clock.tick(30)
    for event in pygame.event.get():
        if (event.type == USEREVENT+1) and (crash == False):
            time -= 1
        if not hasattr(event, 'key'): continue
        down = event.type == KEYDOWN
        if crash == False:
            if event.key == K_RIGHT: car.k_right = down * -5
            elif event.key == K_LEFT: car.k_left = down * 5
            elif event.key == K_UP: car.k_up = down * 2
            elif event.key == K_DOWN: car.k_down = down * -2
            elif event.key == K_SPACE: car.k_left = car.k_right = car.k_down = car.k_up = 0
        elif crash == True and event.key == K_r:
            pygame.quit()
            pygame.display.quit()
            subprocess.call(["python", "carracing.py"])
        if event.key == K_ESCAPE:
            pygame.quit()
            pygame.display.quit()
            subprocess.call(["python", "menu.py"])          
    if time == 0:
        print "TIME OVER"

    # RENDERING
    screen.blit(background_img,(0,0))
    bonus_group.clear(screen, background)
    pad_group.clear(screen, background)
    car_group.clear(screen, background)

    # Display OSD
    pygame.draw.rect(screen,(0,0,0), (0,0,60,height), 0)

    # life P1
    if lifeP1 >0:
        pygame.draw.rect(screen,(255,0,0), (10, height-10, 10, -int(lifeP1/100.0*height/2)), 0)

    # life P2
    if lifeP2 >0:
        pygame.draw.rect(screen,(0,255,0), (25, height-10, 10, -int(lifeP2/100.0*height/2)), 0)

    # life P3
    if lifeP3 >0:
        pygame.draw.rect(screen,(0,0,255), (40, height-10, 10, -int(lifeP3/100.0*height/2)), 0)    

    # display fps
    fpstext = DisplayText("%d fps" % int(clock.get_fps()),basicfont,(255, 0, 0),25,0,5,10)
    fpstext.render()

    # display time
    if (time >= 0):
        timetext = DisplayText("%d" % time,bigfont,(255, 255, 255),27,0,5,50)
        timetext.render()

    car_group.update(deltat)
    # CHECK IF CAR IS LEAVING SCREEN
    if car.position[0] <90:
        car.position = (width, car.position[1])
    elif car.position[0] > width:
        car.position = (90, car.position[1])
    if car.position[1] <0:
        car.position = (car.position[0], height)
    elif car.position[1] > height:
        car.position = (car.position[0], 0)


    # DRAW ALL SPRITES
    all_sprites_list.draw(screen)

    # CHECK COLLISIONS CAR/PADS
    pads = pygame.sprite.spritecollide(car, pad_group, False)
    if pads:
        lifeP1=lifeP1-10
        if lifeP1 != 0:
            car.speed = -car.speed
        else:
            car.src_image = car.car_hit
            car.speed = 0
            car.k_left = car.k_right = car.k_down = car.k_up = 0
            crash = True

    # CHECK IF CAR HAS TAKEN BONUS
    bonus = pygame.sprite.spritecollide(car, bonus_group, False)
    if bonus:
        car.speed = 20 # Speed up car speed
        bonus_group.update(bonus, pygame.image.load("empty.png"))
    if crash == True:
        # Display Game Over
        gameovertext = DisplayText("Game Over",bigfont,(255, 0, 0),width/2,height/2,5,-10)
        gameovertext.render()
        # Display Restart (R-key for PC/MAC users)
        restarttext = DisplayText("Press Start to play again",mediumfont,(255, 0, 0),width/2,height/2,5,30)
        restarttext.render()
    pygame.display.flip()
