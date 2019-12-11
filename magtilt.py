import RPi.GPIO as GPIO
import time
from math import *

## magnetometer/accelerometer is Adafruit_LSM303DLHC
import Adafruit_LSM303
lsm303 = Adafruit_LSM303.LSM303()

## Set RPi GPIO pins to board numbering
GPIO.setmode(GPIO.BOARD)
## Set board pin 7 to pinout
GPIO.setup(7,GPIO.OUT)
## Set pin 7 to pulse width modulation @50 hz
pwm = GPIO.PWM(7,50)
pwm.start(7)
## define rudder left, straight, right
left = 2
straight = 6.7
right = 11.5

while True:
## setup magnetometer/accelerometer to read all
	accel, mag = lsm303.read()
	accel_x, accel_y, accel_z = accel
	mag_x, mag_y, mag_z = mag



## convert magnetometer gauss readings to compass heading
	compass = atan2(mag_y,mag_x) * (180/pi)
	heading = compass
	if compass<0:
		heading+=360
	print('compass = ' + str(heading))

## normalize accelerometer values
	accXnorm = accel_x/sqrt(accel_x * accel_x + accel_y * accel_y + accel_z * accel_z)
	accYnorm = accel_y/sqrt(accel_x * accel_x + accel_y * accel_y + accel_z * accel_z)
## calculate pitch/roll
	pitch = asin(accXnorm)
	roll = -asin(accYnorm/cos(pitch))
## calculate tilt compensated compass
	magXcomp = mag_x * cos(pitch) + mag_z * sin(pitch)
	magYcomp = mag_x*sin(roll)*sin(pitch)+mag_y*cos(roll)+mag_z*sin(roll)*cos(pitch)
	tiltcomp = atan2(magYcomp,magXcomp) * (180/pi)
	if tiltcomp < 0:
		tiltcomp+=360
#	print('tiltcomp = ' + str(tiltcomp))
## setup autopilot
#	if heading < 270:
#		pwm.ChangeDutyCycle(left)
#	if heading > 300:
#		pwm.ChangeDutyCycle(right)
#	if heading < 300 and heading > 270:
#		pwm.ChangeDutyCycle(straight)
	time.sleep(.5)
