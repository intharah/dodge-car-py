import pygame, math, os, sys, subprocess
from pygame.locals import *
from pyscope import pyscope
from SceneBase import *
from Displaytext import DisplayText
from globals import *


class TitleScene(SceneBase):
    def __init__(self, screen, inputpi, settings, width, height, sfx, net):
        SceneBase.__init__(self, screen, inputpi, settings, width, height, sfx, net)
        pygame.font.init()
        self.font = pygame.font.Font('data/coders_crux/coders_crux.ttf', 40)
        pygame.time.set_timer(TIMER2, 1000)
        self.my_car = int(self.settings.get("General", "player"))
        self.blink = 7
        self.p1ready = False
        self.p2ready = False

    def Start(self):
        print "start title"
        self.p1ready = False
        self.p2ready = False        
            
    def Stop(self):
        print "stop title"
        self.p1ready = False
        self.p2ready = False

    
    def ProcessInput(self, events, pressed_keys):
        for event in events:
            if event.type == BTNEVENT:
                self.SwitchToScene('game')
            if event.type == TIMER2:
                self.blink = 7
            if event.type == KEYDOWN:
                if event.key == K_RETURN:
                    '''
                    if (self.my_car == 0):
                        self.p1ready = True
                        self.net.send('0:ready')
                    else: 
                        self.p2ready = True
                        self.net.send('1:ready')
                        # launch game
                    '''
                    self.SwitchToScene('game')
                    
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            elif event.type == QUIT:
                pygame.display.quit()
                sys.exit()
    
    def Update(self):
        if self.blink > 0:
            self.blink = self.blink -1
	    print self.blink
    
    def Render(self, screen, clock, deltat):
        background_img = pygame.image.load("game_logo.png").convert()
        screen.fill((0,0,0))
        screen.blit(background_img,(180,0))
        if self.blink > 0:
            if not self.p1ready:
                p1text = DisplayText(screen,"Press Start",self.font,(255, 255, 255),320,320,0,0)
                p1text.render()
        '''
            if not self.p2ready:
                p1text = DisplayText(screen,"Press Start",self.font,(255, 255, 255),320,370,0,0)
                p1text.render()
        '''
        if self.p1ready:
            p1text = DisplayText(screen,"Ready!",self.font,(255, 255, 255),320,200,0,0)
            p1text.render()
        '''
        if self.p2ready:
            p2text = DisplayText(screen,"Ready!",self.font,(255, 255, 255),320,250,0,0)
            p2text.render()
        '''


