#!/usr/bin/python

import smbus
import time

bus = smbus.SMBus(1)

DEVICE_ADDRESS = 0x54


while True:
    word = bus.read_word_data(DEVICE_ADDRESS, 0)
    print hex(word)
    if word == 0x5500:
        word = bus.read_word_data(DEVICE_ADDRESS, 0)
        if word == 0x55aa:
            checksum = bus.read_word_data(DEVICE_ADDRESS, 0)
            signature = bus.read_word_data(DEVICE_ADDRESS, 0)
            xctr = bus.read_word_data(DEVICE_ADDRESS, 0)
            yctr = bus.read_word_data(DEVICE_ADDRESS, 0)
            width = bus.read_word_data(DEVICE_ADDRESS, 0)
            height = bus.read_word_data(DEVICE_ADDRESS, 0)
            print "signature: ", signature
            print "x ctr: ", xctr
            print "y ctr: ", yctr
            print "width: ", width
            print "height: ", height
            
    time.sleep(0.1)
    




