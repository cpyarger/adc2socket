#!/usr/bin/env python3
# read abelectronics ADC Pi V2 board inputs with repeating reading from each channel 16 bit mode
# uses quick2wire from http://quick2wire.com/ github: https://github.com/quick2wire/quick2wire-python-api
# Requries Python 3 
# GPIO API depends on Quick2Wire GPIO Admin. To install Quick2Wire GPIO Admin, follow instructions at http://github.com/quick2wire/quick2wire-gpio-admin
# I2C API depends on I2C support in the kernel

# Version 1.0  - 09/07/2013
# Version History:
# 1.0 - Initial Release

#
# Usage: changechannel(address, hexvalue) to change to new channel on adc chips
# Usage: getadcreading(address) to return value in volts from selected channel.
#
# address = adc_address1 or adc_address2 - Hex address of I2C chips as configured by board header pins.
import datetime, time
import quick2wire.i2c as i2c
adc_address1 = 0x68
adc_address2 = 0x69

# 16 bit 
varDivisior = 16 # from pdf sheet on adc addresses and config
# 12 bit
varDivisior = 1 # from pdf sheet on adc addresses and config

varMultiplier = (2.4705882/varDivisior)/1000
            
            
with i2c.I2CMaster() as bus:
# 16 bit
#	bus.transaction(i2c.writing_bytes(adc_address1, 0x98))
# 12 bit
	bus.transaction(i2c.writing_bytes(adc_address1, 0x90))
	
	def getadcreading(address):
		h, l ,s = bus.transaction(i2c.reading(address,3))[0]
		while (s & 128):
			h, l, s  = bus.transaction(i2c.reading(address,3))[0]
		# shift bits to product result
		t = (h << 8) | l
		# check if positive or negative number and invert if needed
		if (h > 128):
			t = ~(0x020000 - t)
		return t * varMultiplier
	print ("Time , Data")
	while True:
		print ("%02f" % time.time() + " ,  %02f"  % getadcreading(adc_address1))

