import pygame, math, os, sys, subprocess
from pygame.locals import *
from pyscope import pyscope
from SceneBase import *
from Displaytext import DisplayText
from carracing import *


class TitleScene(SceneBase):
    def __init__(self, screen, inputpi, settings, width, height, sfx):
        SceneBase.__init__(self, screen, inputpi, settings, width, height, sfx)
        pygame.font.init()
        self.font = pygame.font.Font('data/coders_crux/coders_crux.ttf', 40)
        pygame.time.set_timer(TIMER2, 1000)
        self.blink = 30
        self.p1ready = False
        self.p2ready = False

    
    def ProcessInput(self, events, pressed_keys):
        '''if inpi:
            sticky = inpi.getPoty()
            if not sticky is False:
                if sticky < 10.0:
                    print "up"
                    menu.draw(-1)
            elif sticky > 90.0:
                print "down"
                menu.draw(1)
            pygame.display.update()
            if inpi.getStart() or inpi.getB():
                if menu.get_position() == 0:#start the game here
                    pygame.quit()
                    pygame.display.quit()
                    startMenu = subprocess.Popen([sys.executable, "carracing.py"])
                    startMenu.communicate()
        '''
        for event in events:
            if event.type == BTNEVENT:
                self.SwitchToScene(GameScene(self.screen, self.inputpi, self.settings, self.width, self.height, self.sfx))
            if event.type == TIMER2:
                self.blink = 15
            if event.type == KEYDOWN:
                if event.key == K_RETURN:
                    self.p1ready = True
                        # launch game
                    self.SwitchToScene(GameScene(self.screen, self.inputpi, self.settings, self.width, self.height, self.sfx))
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            elif event.type == QUIT:
                pygame.display.quit()
                sys.exit()
    
    def Update(self):
        if self.blink > 0:
            self.blink = self.blink -1
    
    def Render(self, screen, clock, deltat):
        background_img = pygame.image.load("grass.png").convert()
        screen.blit(background_img,(0,0))
        if self.blink > 0:
            if not self.p1ready:
                p1text = DisplayText(screen,"Press Start",self.font,(255, 255, 255),320,200,0,0)
                p1text.render()
            if not self.p2ready:
                p1text = DisplayText(screen,"Press Start",self.font,(255, 255, 255),320,250,0,0)
                p1text.render()
        if self.p1ready:
            p1text = DisplayText(screen,"Ready!",self.font,(255, 255, 255),320,200,0,0)
            p1text.render()
        if self.p2ready:
            p2text = DisplayText(screen,"Ready!",self.font,(255, 255, 255),320,250,0,0)
            p2text.render()



