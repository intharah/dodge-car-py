'''
@author: avalanchy (at) google mail dot com
@version: 0.1; python 2.7; pygame 1.9.2pre; SDL 1.2.14; MS Windows XP SP3
@date: 2012-04-08
@license: This document is under GNU GPL v3

README on the bottom of document.

@font: from http://www.dafont.com/coders-crux.font
      more abuot license you can find in data/coders-crux/license.txt
'''
 
import pygame, math, os, sys, subprocess
from pygame.locals import *
from pyscope import pyscope

#FX and sounds
pygame.mixer.pre_init(44100, 16, 2, 2048) # setup mixer to avoid sound lag
pygame.init()

pygame.mixer.music.load(os.path.join('sounds', 'highway_slaughter.ogg'))#load music
#jump = pygame.mixer.Sound(os.path.join('sounds','jump.wav'))  #load sound
#fail = pygame.mixer.Sound(os.path.join('sounds','fail.wav'))  #load sound
    
#music is already the name of the music object
#pygame.mixer.music.play(loops=0, start=0.0): return None
pygame.mixer.music.play(-1) # play endless

width = 640
height = 480
inpi = False

if (sys.platform == "darwin") or (sys.platform == "win32") or (not os.uname()[4].startswith("arm")):
    surface = pygame.display.set_mode((width, height)) #0,6671875 and 0,(6) of HD resoultion
else:
    scope = pyscope()
    surface = scope.screen
    width = surface.get_size()[0]
    height = surface.get_size()[1]
    from inputpi import inputpi
    inpi = inputpi()

if not pygame.display.get_init():
    pygame.display.init()

if not pygame.font.get_init():
    pygame.font.init()

background_img = pygame.image.load("grass.png").convert()

class Menu:
    lista = []
    pola = []
    rozmiar_fontu = 32
    font_path = 'data/coders_crux/coders_crux.ttf'
    font = pygame.font.Font
    dest_surface = pygame.Surface
    ilosc_pol = 0
    kolor_tla = (51,51,51,0)
    kolor_tekstu =  (255, 255, 153)
    kolor_zaznaczenia = (153,102,255)
    pozycja_zaznaczenia = 0
    pozycja_wklejenia = (0,0)
    menu_width = 0
    menu_height = 0

    class Pole:
        tekst = ''
        pole = pygame.Surface
        pole_rect = pygame.Rect
        zaznaczenie_rect = pygame.Rect

    def move_menu(self, top, left):
        self.pozycja_wklejenia = (top,left) 

    def set_colors(self, text, selection, background):
        self.kolor_tla = background
        self.kolor_tekstu =  text
        self.kolor_zaznaczenia = selection
        
    def set_fontsize(self,font_size):
        self.rozmiar_fontu = font_size
        
    def set_font(self, path):
        self.font_path = path
        
    def get_position(self):
        return self.pozycja_zaznaczenia
    
    def init(self, lista, dest_surface):
        self.lista = lista
        self.dest_surface = dest_surface
        self.ilosc_pol = len(self.lista)
        self.stworz_strukture()        
        
    def draw(self,przesun=0):
        if przesun:
            self.pozycja_zaznaczenia += przesun 
            if self.pozycja_zaznaczenia == -1:
                self.pozycja_zaznaczenia = self.ilosc_pol - 1
            self.pozycja_zaznaczenia %= self.ilosc_pol
        menu = pygame.Surface((self.menu_width, self.menu_height),pygame.SRCALPHA)
        #menu.fill(self.kolor_tla)
        menu.blit(background_img,(0,0))
        zaznaczenie_rect = self.pola[self.pozycja_zaznaczenia].zaznaczenie_rect
        pygame.draw.rect(menu,self.kolor_zaznaczenia,zaznaczenie_rect)

        for i in xrange(self.ilosc_pol):
            menu.blit(self.pola[i].pole,self.pola[i].pole_rect)
        self.dest_surface.blit(menu,self.pozycja_wklejenia)
        return self.pozycja_zaznaczenia

    def stworz_strukture(self):
        przesuniecie = 0
        self.menu_height = 0
        self.font = pygame.font.Font(self.font_path, self.rozmiar_fontu)
        for i in xrange(self.ilosc_pol):
            self.pola.append(self.Pole())
            self.pola[i].tekst = self.lista[i]
            self.pola[i].pole = self.font.render(self.pola[i].tekst, 1, self.kolor_tekstu)

            self.pola[i].pole_rect = self.pola[i].pole.get_rect()
            przesuniecie = int(self.rozmiar_fontu * 0.2)

            height = self.pola[i].pole_rect.height
            self.pola[i].pole_rect.left = przesuniecie
            self.pola[i].pole_rect.top = przesuniecie+(przesuniecie*2+height)*i

            width = self.pola[i].pole_rect.width+przesuniecie*2
            height = self.pola[i].pole_rect.height+przesuniecie*2            
            left = self.pola[i].pole_rect.left-przesuniecie
            top = self.pola[i].pole_rect.top-przesuniecie

            self.pola[i].zaznaczenie_rect = (left,top ,width, height)
            if width > self.menu_width:
                    self.menu_width = width
            self.menu_height += height
        x = self.dest_surface.get_rect().centerx - self.menu_width / 2
        y = self.dest_surface.get_rect().centery - self.menu_height / 2
        mx, my = self.pozycja_wklejenia
        self.pozycja_wklejenia = (x+mx, y+my) 


if __name__ == "__main__":
    import sys
    #surface.fill((51,51,51))
    surface.blit(background_img,(0,0))
    '''First you have to make an object of a *Menu class.
    *init take 2 arguments. List of fields and destination surface.
    Then you have a 4 configuration options:
    *set_colors will set colors of menu (text, selection, background)
    *set_fontsize will set size of font.
    *set_font take a path to font you choose.
    *move_menu is quite interseting. It is only option which you can use before 
    and after *init statement. When you use it before you will move menu from 
    center of your surface. When you use it after it will set constant coordinates. 
    Uncomment every one and check what is result!
    *draw will blit menu on the surface. Be carefull better set only -1 and 1 
    arguments to move selection or nothing. This function will return actual 
    position of selection.
    *get_postion will return actual position of seletion. '''
    menu = Menu()#necessary
    #menu.set_colors((255,255,255), (0,0,255), (0,0,0))#optional
    #menu.set_fontsize(64)#optional
    #menu.set_font('data/couree.fon')#optional
    #menu.move_menu(100, 99)#optional
    menu.init(['Start','Highscores','Credits'], surface)#necessary
    #menu.move_menu(0, 0)#optional
    menu.draw()#necessary
    
    pygame.key.set_repeat(199,69)#(delay,interval)
    pygame.display.update()
    while 1:
        if inpi:
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
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_UP:
                    menu.draw(-1) #here is the Menu class function
                if event.key == K_DOWN:
                    menu.draw(1) #here is the Menu class function
                if event.key == K_RETURN:
                    if menu.get_position() == 0:#start the game here
                        pygame.quit()
                        pygame.display.quit()
                        startMenu = subprocess.Popen([sys.executable, "carracing.py"])
                        startMenu.communicate()
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                pygame.display.update()
            elif event.type == QUIT:
                pygame.display.quit()
                sys.exit()
        pygame.time.wait(100)
        
