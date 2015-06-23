# INTIALISATION
import pygame, math, os, sys, subprocess, random, pdb, ConfigParser
from pygame.locals import *
from pyscope import pyscope
from SceneBase import *
from title import *
from globals import *

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
sfx = {'drive': drive, 'drift': drift, 'speed': speed, 'energy': energy, 'hit': hit, 'explosion': explosion}

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
fps = 30

pygame.time.set_timer(TIMER1, 1000)


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

if not pygame.display.get_init():
    pygame.display.init()

if not pygame.font.get_init():
    pygame.font.init()

run_game(pygame, screen, inpi, settings, width, height, sfx, fps, TitleScene(screen, inpi, settings, width, height, sfx))
