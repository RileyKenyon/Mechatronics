#!/usr/bin/python

import smbus
import time

bus = smbus.SMBus(1)
time.sleep(1);

DEVICE_ADDRESS = 0x04 

cmd = '<MOT-CWO|100>'
cmd_list = list(cmd)
cmd_ord = [ord(i) for i in cmd_list]
msg = bus.write_i2c_block_data(DEVICE_ADDRESS,0,cmd_ord)


