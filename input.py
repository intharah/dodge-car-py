#!/usr/bin/env python

# Written by Limor "Ladyada" Fried for Adafruit Industries, (c) 2015
# This code is released into the public domain

import time
import os
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
DEBUG = 1

GPIO.setup(4, GPIO.IN, pull_up_down=GPIO.PUD_UP)


# read SPI data from MCP3008 chip, 8 possible adc's (0 thru 7)
def readadc(adcnum, clockpin, mosipin, misopin, cspin):
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

# change these as desired - they're the pins connected from the
# SPI port on the ADC to the Cobbler
SPICLK = 18
SPIMISO = 23
SPIMOSI = 24
SPICS = 25

# set up the SPI interface pins
GPIO.setup(SPIMOSI, GPIO.OUT)
GPIO.setup(SPIMISO, GPIO.IN)
GPIO.setup(SPICLK, GPIO.OUT)
GPIO.setup(SPICS, GPIO.OUT)

# 10k trim pot connected to adc #0
potx = 0;
poty = 1;

last_readx = 0       # this keeps track of the last potentiometer value
last_ready = 0
tolerance = 5       # to keep from being jittery we'll only change
                    # volume when the pot has moved more than 5 'counts'

while True:
        # we'll assume that the pot didn't move
        trim_pot_changedx = False
	trim_pot_changedy = False

        # read the analog pin
        trim_potx = readadc(potx, SPICLK, SPIMOSI, SPIMISO, SPICS)
	trim_poty = readadc(poty, SPICLK, SPIMOSI, SPIMISO, SPICS)
        # how much has it changed since the last read?
        pot_adjustx = abs(trim_potx - last_readx)
	pot_adjusty = abs(trim_poty - last_ready)


        if ( pot_adjustx > tolerance ):
               trim_pot_changedx = True

	if (pot_adjusty > tolerance ):
               trim_pot_changedy = True

        if ( trim_pot_changedx ):
                valx = trim_potx / 10.24           # convert 10bit adc0 (0-1024) trim pot read into 0-100 volume level
		print "x:", valx

                # save the potentiometer reading for the next loop
                last_readx = trim_potx

	if (trim_pot_changedy ):
		valy = trim_poty / 10.24
		print "y:", valy

		last_ready = trim_poty
	but0 = GPIO.input(4)
	if but0 == False:
		print "but0 pressed"
        # hang out and do nothing for a half second
        time.sleep(0.1)
