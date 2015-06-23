#!/usr/bin/env python

# Written by Limor "Ladyada" Fried for Adafruit Industries, (c) 2015
# This code is released into the public domain

import time
import os
import RPi.GPIO as GPIO


class inputpi:
	# change these as desired - they're the pins connected from the
	# SPI port on the ADC to the Cobbler
	SPICLK = 18
	SPIMISO = 23
	SPIMOSI = 24
	SPICS = 25


	# 10k trim pot connected to adc #0
	potx = 1;
	poty = 0;

	last_readx = 0       # this keeps track of the last potentiometer value
	last_ready = 0
	tolerance = 5       # to keep from being jittery we'll only change
	                    # volume when the pot has moved more than 5 'counts'

	DEBUG = 0

	def __init__(self):	
		btns_names = ['select', 'start', 'y', 'x', 'b', 'l', 'r', 'a', 'stick']
		btns_pins = [2, 3, 4, 14, 15, 17, 27, 22, 10]

		GPIO.setwarnings(False)
		GPIO.setmode(GPIO.BCM)

		GPIO.setup(self.bselect, GPIO.IN, pull_up_down=GPIO.PUD_UP)
		GPIO.setup(self.bstart, GPIO.IN, pull_up_down=GPIO.PUD_UP)
		GPIO.setup(self.by, GPIO.IN, pull_up_down=GPIO.PUD_UP)
		GPIO.setup(self.bx, GPIO.IN, pull_up_down=GPIO.PUD_UP)
		GPIO.setup(self.bb, GPIO.IN, pull_up_down=GPIO.PUD_UP)
		GPIO.setup(self.bl, GPIO.IN, pull_up_down=GPIO.PUD_UP)
		GPIO.setup(self.br, GPIO.IN, pull_up_down=GPIO.PUD_UP)
		GPIO.setup(self.ba, GPIO.IN, pull_up_down=GPIO.PUD_UP)
		GPIO.setup(self.bstick, GPIO.IN, pull_up_down=GPIO.PUD_UP)
		# set up the SPI interface pins
		GPIO.setup(self.SPIMOSI, GPIO.OUT)
		GPIO.setup(self.SPIMISO, GPIO.IN)
		GPIO.setup(self.SPICLK, GPIO.OUT)
		GPIO.setup(self.SPICS, GPIO.OUT)




	# read SPI data from MCP3008 chip, 8 possible adc's (0 thru 7)
	def readadc(self, adcnum):
		clockpin = self.SPICLK
		mosipin = self.SPIMOSI
		misopin = self.SPIMISO
		cspin = self.SPICS
	        if ((adcnum > 7) or (adcnum < 0)):
	                return -1
	        GPIO.output(cspin, True)
	        GPIO.output(clockpin, False)  # start clock low
	        GPIO.output(cspin, False)     # bring CS low
	        commandout = adcnum
	        commandout |= 0x18  # start bit + single-ended bit
	        commandout <<= 3    # we only need to send 5 bits here
	        for i in range(5):
	                if (commandout & 0x80):
	                        GPIO.output(mosipin, True)
	                else:
	                        GPIO.output(mosipin, False)
	                commandout <<= 1
	                GPIO.output(clockpin, True)
               		GPIO.output(clockpin, False)
        		adcout = 0
       		# read in one empty bit, one null bit and 10 ADC bits
       		for i in range(12):
               		GPIO.output(clockpin, True)
               		GPIO.output(clockpin, False)
               		adcout <<= 1
               		if (GPIO.input(misopin)):
                       		adcout |= 0x1

       		GPIO.output(cspin, True)
        
       		adcout >>= 1       # first bit is 'null' so drop it
       		return adcout

	def getPotx(self):
	        # we'll assume that the pot didn't move
        	trim_pot_changedx = False
	        # read the analog pin
        	trim_potx = self.readadc(self.potx)
		# how much has it changed since the last read?
        	pot_adjustx = abs(trim_potx - self.last_readx)
	        if ( pot_adjustx > self.tolerance ):
               		trim_pot_changedx = True
	        if ( trim_pot_changedx ):
 	      	        valx = trim_potx / 10.24           # convert 10bit adc0 (0-1024) trim pot read into 0-100 volume level
			if self.DEBUG == 1:
				print "x:", valx

        	        # save the potentiometer reading for the next loop
               		self.last_readx = trim_potx
			return valx
		else:
			return False

	def getPoty(self):
		trim_pot_changedy = False
		trim_poty = self.readadc(self.poty)
		pot_adjusty = abs(trim_poty - self.last_ready)
		if (pot_adjusty > self.tolerance ):
               		trim_pot_changedy = True

		if (trim_pot_changedy ):
			valy = trim_poty / 10.24
			if self.DEBUG ==1:
				print "y:", valy

			self.last_ready = trim_poty
			return valy
		else:
			return False


	def sendEvents(self):
		stickx = self.getPotx()
		sticky = self.getPoty()
		if not stickx is False:
			stickxevent = pygame.event.Event(STICKEVENT, axis=0, value=stickx)
			pygame.event.post(stickxevent)
		if not sticky is False:
			stickyevent = pygame.event.Event(STICKEVENT, axis=1, value=sticky)
			pygame.event.post(stickyevent)
		for i in btns_names:
			if not GPIO.input(i):
				btnevent = pygame.event.Event(BTNEVENT, btn=btns_pins[i])

