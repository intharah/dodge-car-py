# INTIALISATION
import pygame, math, os, sys, subprocess, random, pdb, ConfigParser
from pygame.locals import *
from pyscope import pyscope
from SceneBase import *
from Displaytext import DisplayText
from globals import *


class PadSprite(pygame.sprite.Sprite):
    def __init__(self,number,normal, screen):
        self.screen = screen
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)
        # Load the image
        self.image = normal
        self.number = number
        self.position = self.pseudoRandomPosition()
        self.rect = self.image.get_rect()
        self.rect.center = self.position
    def update(self, hit_list, normal, hit):
        if self in hit_list: self.image = hit
        else: self.image = normal
    def reset(self):
        self.position = self.pseudoRandomPosition()
        self.rect = self.image.get_rect()
        self.rect.center = self.position
    def pseudoRandomPosition(self):
        center = self.screen.get_rect().center
        found = False
        result = center
        while not found:
            x = random.randint(100, 600)
            y = random.randint(0, 400)
            dist = math.sqrt((center[0] -x)**2 + (center[0] -y) ** 2)
            print dist
            if dist > 150:
                result = (x,y)
                print result
                found = True
        return result
    
    
class CarSprite(pygame.sprite.Sprite):
    MAX_FORWARD_SPEED = 10
    MAX_REVERSE_SPEED = 10
    ACCELERATION = 2
    TURN_SPEED = 5

    car_hit = pygame.image.load("pad_hit.png")

    def __init__(self, position, player):
        self.player = player
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
    def reset(self):
        if (self.player == 0):
            self.car_img = pygame.image.load("carr.png")
        elif (self.player ==1):
            self.car_img = pygame.image.load("carg.png")
        elif (self.player ==2):
            self.car_img = pygame.image.load("carb.png")
        

class GameScene(SceneBase):
    def __init__(self, screen, inputpi, settings, width, height, sfx, net):
        SceneBase.__init__(self, screen, inputpi, settings, width, height, sfx, net)
        self.lifeP1 = 100
        self.lifeP2 = 100


        self.time = 99
        pygame.time.set_timer(TIMER1, 1000)
        self.crash = False
        self.block_list = pygame.sprite.Group()
         
        # This is a list of every sprite.
        # All blocks and the player block as well.
        self.all_sprites_list = pygame.sprite.Group()
        # Order correctly the sprites in group
        self.all_sprites_list = pygame.sprite.OrderedUpdates()
        
        # CREATE PADS
        pads = [
            PadSprite(1,pygame.image.load("rock.png"), self.screen),
            PadSprite(2,pygame.image.load("rock.png"), self.screen)
        ]
        self.pad_group = pygame.sprite.RenderPlain(*pads)
        self.all_sprites_list.add(*pads)

        # CREATE LIFE BONUS
        life = PadSprite(1,pygame.image.load("life.png"), self.screen)
        self.life_group = pygame.sprite.RenderPlain(life)
        self.all_sprites_list.add(self.life_group)

        # CREATE SPEED BONUS
        bonus = PadSprite(1,pygame.image.load("bonus.png"), self.screen)
        self.bonus_group = pygame.sprite.RenderPlain(bonus)
        self.all_sprites_list.add(self.bonus_group)

        # CREATE GREASE ITEM
        grease = [
            PadSprite(1,pygame.image.load("grease.png"), self.screen),
            PadSprite(2,pygame.image.load("grease.png"), self.screen)
        ]
        self.grease_group = pygame.sprite.RenderPlain(*grease)
        self.all_sprites_list.add(self.grease_group)

        # CREATE A CAR AND RUN
        my_car_num = int(self.settings.get("General", "player"))
        if my_car_num == 0:
            rect = self.screen.get_rect().center
        else:
            rect = (self.screen.get_rect().center[0] -50, self.screen.get_rect().center[1])
        self.car = CarSprite(rect, my_car_num)
        self.car_group = pygame.sprite.RenderPlain(self.car)
        self.all_sprites_list.add(self.car_group)

        # CREATE OTHER CARS
        pos_car2 = self.screen.get_rect().center
        if my_car_num == 1:
            pos_car2 = self.screen.get_rect().center
        else:
            pos_car2 = (self.screen.get_rect().center[0] -50, self.screen.get_rect().center[1] ) 
     
        self.car2 = CarSprite(pos_car2, (my_car_num +1) % 2)
        ennemies = [
            self.car2
        ]
        self.ennemies_group = pygame.sprite.RenderPlain(*ennemies)
        self.all_sprites_list.add(self.ennemies_group)

        pygame.font.init()
        self.basicfont = pygame.font.Font('data/coders_crux/coders_crux.ttf', 20)
        self.mediumfont = pygame.font.Font('data/coders_crux/coders_crux.ttf', 40)
        self.bigfont = pygame.font.Font('data/coders_crux/coders_crux.ttf', 70)
        self.play_explosion_sound = False
        self.explosion_isPlayed = 0 

        self.background = pygame.Surface(self.screen.get_size())
        self.background = self.background.convert()
        self.background.fill((250, 250, 250))
        self.background_img = pygame.image.load("grass.png").convert()

    def Start(self):
        my_car_num = int(self.settings.get("General", "player"))
        print "start game"
        self.lifeP1 = 100
        self.lifeP2 = 100


        self.time = 99
        self.crash = False
        for i in self.all_sprites_list.sprites():
            i.reset()
            
        if my_car_num == 0:
            rect = self.screen.get_rect().center
        else:
            rect = (rect.center[0] -50, rect.center[1])
        self.car.position = rect
        self.car.direction = 0

        if my_car_num == 1:
            pos_car2 = self.screen.get_rect().center
        else:
            pos_car2 = (self.screen.get_rect().center[0] -50, self.screen.get_rect().center[1] ) 
        self.car2.position = pos_car2
        self.car2.direction = 0
        
        
            
    def Stop(self):
        print "stop game"

    def ProcessInput(self, events, pressed_keys):
        '''
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
        '''
        for event in events:
            if (event.type == TIMER1) and (self.crash == False):
                self.time -= 1
            if not hasattr(event, 'key'): continue
            down = event.type == KEYDOWN
            if self.crash == False:
                self.explosion_isPlayed = 0 
                self.car.src_image = pygame.transform.rotate(self.car.car_img, 0) #reset rotation for car if drifted
                if event.key == K_RIGHT:
                    self.car.k_right = down * -5
                    self.sfx['drive'].play()
                elif event.key == K_LEFT:
                    self.car.k_left = down * 5
                    self.sfx['drive'].play()
                elif event.key == K_UP:
                    self.car.k_up = down * 2
                    self.sfx['drive'].play()
                elif event.key == K_DOWN:
                    self.car.k_down = down * -2
                    self.sfx['drive'].play()
                elif event.key == K_SPACE: self.car.k_left = self.car.k_right = self.car.k_down = self.car.k_up = 0
            elif self.crash == True and event.key == K_r:
                print "restart"
                self.SwitchToScene('title')
                
    
    def Update(self):
        if self.time == 0:
            print "TIME OVER"
        # CHECK IF CAR IS LEAVING SCREEN
        if self.car.position[0] <90:
            self.car.position = (self.width, self.car.position[1])
        elif self.car.position[0] > self.width:
            self.car.position = (90, self.car.position[1])
        if self.car.position[1] <0:
            self.car.position = (self.car.position[0], self.height)
        elif self.car.position[1] > self.height:
            self.car.position = (self.car.position[0], 0)

        # CHECK COLLISIONS CAR/PADS
        pads = pygame.sprite.spritecollide(self.car, self.pad_group, False)
        if pads:
            self.lifeP1=self.lifeP1-10
            self.sfx['hit'].play()
            if self.lifeP1 >= 0:
                self.car.speed = -self.car.speed
            else:
                self.car.src_image = self.car.car_hit
                self.car.speed = 0
                self.car.k_left = self.car.k_right = self.car.k_down = self.car.k_up = 0
                self.crash = True

            
        # CHECK COLLISIONS CAR/CAR
        enn = pygame.sprite.spritecollide(self.car, self.ennemies_group, False)
        if enn:
            #self.lifeP1=self.lifeP1-10
            self.sfx['hit'].play()
            #print self.car.direction
            #print enn[0].direction
            if self.lifeP1 != 0:
                self.car.speed = -self.car.speed
                angleA = math.radians(self.car.direction)
                angleB = math.radians(enn[0].direction)
                angleNormal = math.atan2(self.car.position[1]-enn[0].position[1], self.car.position[0]-enn[0].position[0])
                degatA = int(math.fabs(angleNormal-angleA)* 3.0)
                degatB = int((2*math.pi - math.fabs(angleNormal-angleB))*3.0)
                print "degatA %d" % degatA
                print "degatB %d" % degatB
                self.lifeP1=self.lifeP1-degatA
                self.lifeP2=self.lifeP2-degatB
                
            else:
                self.car.src_image = self.car.car_hit
                self.car.speed = 0
                self.car.k_left = self.car.k_right = self.car.k_down = self.car.k_up = 0
                self.crash = True
            if self.lifeP2 <=0:
                self.crash = True            

        # CHECK IF CAR HAS TAKEN BONUS
        bonus = pygame.sprite.spritecollide(self.car, self.bonus_group, False)
        if bonus:
            self.car.speed = self.car.MAX_FORWARD_SPEED # Speed up car speed
            self.sfx['speed'].play()
            self.bonus_group.remove(bonus)
            self.all_sprites_list.remove(bonus)

        # CHECK IF CAR IS DRIFTING
        grease = pygame.sprite.spritecollide(self.car, self.grease_group, False)
        if grease:
            self.car.src_image = pygame.transform.rotate(self.car.car_img, 45) # Drifting car
            self.sfx['drift'].play()

        # CHECK IF LIFE IS UP
        life = pygame.sprite.spritecollide(self.car, self.life_group, False)
        if life:
            self.lifeP1=100 # Refill power bar
            self.sfx['energy'].play()
            self.life_group.remove(life)
            self.all_sprites_list.remove(life)
            life = False

        # LIFE LEVEL TO 0
        if self.play_explosion_sound and self.explosion_isPlayed == 0:
            self.play_explosion_sound = False
            self.explosion_isPlayed += 1
            self.sfx['explosion'].play()
    
    def Render(self, screen, clock, deltat):
        # For the sake of brevity, the title scene is a blank red screen

        self.screen.blit(self.background_img,(0,0))

        self.bonus_group.clear(self.screen, self.background)
        self.grease_group.clear(self.screen, self.background)
        self.pad_group.clear(self.screen, self.background)
        self.car_group.clear(self.screen, self.background)
        self.ennemies_group.clear(self.screen, self.background)

        # Display OSD
        pygame.draw.rect(self.screen,(0,0,0), (0,0,60,self.height), 0)

        # life P1
        if self.lifeP1 >0:
            pygame.draw.rect(self.screen,(255,0,0), (10, self.height-10, 10, -int(self.lifeP1/100.0*self.height/2)), 0)

        # life P2
        if self.lifeP2 >0:
            pygame.draw.rect(self.screen,(0,255,0), (25, self.height-10, 10, -int(self.lifeP2/100.0*self.height/2)), 0)

        # display fps
        fpstext = DisplayText(self.screen,"%d fps" % int(clock.get_fps()),self.basicfont,(255, 0, 0),25,0,5,10)
        fpstext.render()

        # display time
        if (self.time >= 0):
            timetext = DisplayText(self.screen,"%d" % self.time,self.bigfont,(255, 255, 255),27,0,5,50)
            timetext.render()
        
        if self.time <= 0:
            self.crash = True

        self.car_group.update(deltat)
        self.ennemies_group.update(deltat)

        # DRAW ALL SPRITES
        self.all_sprites_list.draw(self.screen)

        if self.crash == True:
            #Stop sfx and increase volume
            self.sfx['hit'].stop()
            self.play_explosion_sound = True
            pygame.mixer.music.set_volume(0.7)
            message = ""
            if (self.time <= 0):
                message = "Time over!"
            elif (self.lifeP1 >0 and self.lifeP2 <=0):
                message = "You win!"
            elif (self.lifeP1 <= 0 and self.lifeP2 >0):
                message = "You lose!"
            elif self.lifeP1 == 0 and self.lifeP2 ==0:
                message = "Draw game!"
                
            # Display Game Over
            gameovertext = DisplayText(self.screen,message,self.bigfont,(255, 0, 0),self.width/2,self.height/2,5,-10)
            gameovertext.render()
            # Display Restart (R-key for PC/MAC users)
            restarttext = DisplayText(self.screen,"Press Start to play again",self.mediumfont,(255, 0, 0),self.width/2,self.height/2,5,30)
            restarttext.render()
