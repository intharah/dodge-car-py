# INTIALISATION
import pygame, math, os, sys, subprocess, random, pdb, ConfigParser
from pygame.locals import *
from pyscope import pyscope

#load Settings
settings = ConfigParser.ConfigParser()
settings.read("settings.ini")


#FX and sounds
pygame.mixer.pre_init(44100,-16,1, 512) # setup mixer to avoid sound lag
pygame.init()

pygame.mixer.music.load(os.path.join('sounds', 'highway_slaughter.ogg'))#load music
drive = pygame.mixer.Sound(os.path.join('sounds','drive.wav'))  #load sound
drift = pygame.mixer.Sound(os.path.join('sounds','drift.wav'))  #load sound
speed = pygame.mixer.Sound(os.path.join('sounds','speed.wav'))  #load sound
energy = pygame.mixer.Sound(os.path.join('sounds','energy.wav'))  #load sound
hit = pygame.mixer.Sound(os.path.join('sounds','hit.wav'))  #load sound
explosion = pygame.mixer.Sound(os.path.join('sounds','explosion.wav'))  #load sound

#fail = pygame.mixer.Sound(os.path.join('sounds','fail.wav'))  #load sound
    
#music is already the name of the music object
#pygame.mixer.music.play(loops=0, start=0.0): return None
pygame.mixer.music.set_volume(0.6)
pygame.mixer.music.play(-1) # play endless
drive.set_volume(0.4)
drift.set_volume(0.2)
play_explosion_sound = False
explosion_isPlayed = 0

width = 640
height = 480

lifeP1 = 100
lifeP2 = 100
lifeP3 = 100

time = 99
pygame.time.set_timer(USEREVENT+1, 1000)
inpi = False

if (sys.platform == "darwin") or (sys.platform == "win32") or (not os.uname()[4].startswith("arm")):
    screen = pygame.display.set_mode((width, height))
else:
    scope = pyscope()
    screen = scope.screen
    width = screen.get_size()[0]
    height = screen.get_size()[1]
    from inputpi import inputpi
    inpi = inputpi()

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
# Order correctly the sprites in group
all_sprites_list = pygame.sprite.OrderedUpdates()

class DisplayText:
    def __init__(self,message,font_type,color,posX,posY,marginX,marginY):
        self.msg = font_type.render(message, True, color)
        self.msgRect = self.msg.get_rect()
        self.msgRect.centerx = posX + marginX
        self.msgRect.centery = posY + marginY

    def render(self):
        screen.blit(self.msg, self.msgRect)

class PadSprite(pygame.sprite.Sprite):
    def __init__(self,number,normal):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)
        # Load the image
        self.image = normal
        self.number = number
        self.position = (random.randint(100, 640), random.randint(0, 480))
        self.rect = self.image.get_rect()
        self.rect.center = self.position
    def update(self, hit_list, normal, hit):
        if self in hit_list: self.image = hit
        else: self.image = normal
    
class CarSprite(pygame.sprite.Sprite):
    MAX_FORWARD_SPEED = 10
    MAX_REVERSE_SPEED = 10
    ACCELERATION = 2
    TURN_SPEED = 5

    car_hit = pygame.image.load("pad_hit.png")

    def __init__(self, position, player):
        if (player == 0):
            self.car_img = pygame.image.load("carr.png")
        elif (player ==1):
            self.car_img = pygame.image.load("carg.png")
        elif (player ==2):
            self.car_img = pygame.image.load("carb.png")
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

# CREATE PADS
pads = [
    PadSprite(1,pygame.image.load("rock.png")),
    PadSprite(2,pygame.image.load("rock.png"))
]
pad_group = pygame.sprite.RenderPlain(*pads)
all_sprites_list.add(*pads)

# CREATE LIFE BONUS
life = PadSprite(1,pygame.image.load("life.png"))
life_group = pygame.sprite.RenderPlain(life)
all_sprites_list.add(life_group)

# CREATE SPEED BONUS
bonus = PadSprite(1,pygame.image.load("bonus.png"))
bonus_group = pygame.sprite.RenderPlain(bonus)
all_sprites_list.add(bonus_group)

# CREATE GREASE ITEM
grease = [
    PadSprite(1,pygame.image.load("grease.png")),
    PadSprite(2,pygame.image.load("grease.png"))
]
grease_group = pygame.sprite.RenderPlain(*grease)
all_sprites_list.add(grease_group)

# CREATE A CAR AND RUN
my_car_num = int(settings.get("General", "player"))
rect = screen.get_rect()
car = CarSprite(rect.center, my_car_num)
car_group = pygame.sprite.RenderPlain(car)
all_sprites_list.add(car_group)

# CREATE OTHER CARS
pos_car2 = rect.center
car2 = CarSprite((rect.center[0] -50, rect.center[1]), (my_car_num +1) % 3)
car3 = CarSprite((rect.center[0] +50, rect.center[1]), (my_car_num +2) % 3)
ennemies = [
    car2,
    car3
]
ennemies_group = pygame.sprite.RenderPlain(*ennemies)
all_sprites_list.add(ennemies_group)

pygame.font.init()
basicfont = pygame.font.Font('data/coders_crux/coders_crux.ttf', 20)
mediumfont = pygame.font.Font('data/coders_crux/coders_crux.ttf', 40)
bigfont = pygame.font.Font('data/coders_crux/coders_crux.ttf', 70)


while 1:
    # USER INPUT
    deltat = clock.tick(30)

    if inpi:
        stickx = inpi.getPotx()
        sticky = inpi.getPoty()
        if not stickx is False:
            if stickx > 50.0:
                car.k_right = 0-int(round((stickx / 10.0)-5.0))
                car.k_left = 0
            else:
                car.k_left = 0-int(round((stickx / 10.0)-5.0))
                car.k_right = 0

        car.k_up = inpi.getB() *2
        car.k_down = inpi.getA() * -2

        if crash == True and inpi.getStart():
            pygame.quit()
            pygame.display.quit()

            restart = subprocess.Popen([sys.executable, "carracing.py"])
            restart.communicate()

    for event in pygame.event.get():
        if (event.type == USEREVENT+1) and (crash == False):
            time -= 1
        if not hasattr(event, 'key'): continue
        down = event.type == KEYDOWN
        if crash == False:
            explosion_isPlayed = 0 
            car.src_image = pygame.transform.rotate(car.car_img, 0) #reset rotation for car if drifted
            if event.key == K_RIGHT:
                car.k_right = down * -5
                drive.play()
            elif event.key == K_LEFT:
                car.k_left = down * 5
                drive.play()
            elif event.key == K_UP:
                car.k_up = down * 2
                drive.play()
            elif event.key == K_DOWN:
                car.k_down = down * -2
                drive.play()
            elif event.key == K_SPACE: car.k_left = car.k_right = car.k_down = car.k_up = 0
        elif crash == True and event.key == K_r:
            pygame.quit()
            pygame.display.quit()
            restart = subprocess.Popen([sys.executable, "carracing.py"])
            restart.communicate()
        if event.key == K_ESCAPE:
            pygame.quit()
            pygame.display.quit()
            # pdb.set_trace() #DEBUG
            gotoMenu = subprocess.Popen([sys.executable, "menu.py"])
            gotoMenu.communicate()
    if time == 0:
        print "TIME OVER"

    # RENDERING
    screen.blit(background_img,(0,0))
    bonus_group.clear(screen, background)
    grease_group.clear(screen, background)
    pad_group.clear(screen, background)
    car_group.clear(screen, background)
    ennemies_group.clear(screen, background)

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
    ennemies_group.update(deltat)
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
        hit.play()
        if lifeP1 != 0:
            car.speed = -car.speed
        else:
            car.src_image = car.car_hit
            car.speed = 0
            car.k_left = car.k_right = car.k_down = car.k_up = 0
            crash = True
            
    # CHECK COLLISIONS CAR/CAR
    enn = pygame.sprite.spritecollide(car, ennemies_group, False)
    if enn:
        lifeP1=lifeP1-10
        hit.play()
        print car.direction
        print enn[0].direction
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
        car.speed = car.MAX_FORWARD_SPEED # Speed up car speed
        speed.play()
        bonus_group.remove(bonus)
        all_sprites_list.remove(bonus)

    # CHECK IF CAR IS DRIFTING
    grease = pygame.sprite.spritecollide(car, grease_group, False)
    if grease:
        car.src_image = pygame.transform.rotate(car.car_img, 45) # Drifting car
        drift.play()

    # CHECK IF LIFE IS UP
    life = pygame.sprite.spritecollide(car, life_group, False)
    if life:
        lifeP1=100 # Refill power bar
        energy.play()
        life_group.remove(life)
        all_sprites_list.remove(life)
        life = False
  
    # LIFE LEVEL TO 0
    if play_explosion_sound and explosion_isPlayed == 0:
        play_explosion_sound = False
        explosion_isPlayed += 1
        explosion.play()
    if crash == True:
        #Stop sfx and increase volume
        hit.stop()
        play_explosion_sound = True
        pygame.mixer.music.set_volume(0.7)
        # Display Game Over
        gameovertext = DisplayText("Game Over",bigfont,(255, 0, 0),width/2,height/2,5,-10)
        gameovertext.render()
        # Display Restart (R-key for PC/MAC users)
        restarttext = DisplayText("Press Start to play again",mediumfont,(255, 0, 0),width/2,height/2,5,30)
        restarttext.render()
    pygame.display.flip()
