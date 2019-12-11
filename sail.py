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
degrees = (right - left)/180


while True:
## setup magnetometer/accelerometer to read all
	accel, mag = lsm303.read()
	accel_x, accel_y, accel_z = accel
	mag_x, mag_y, mag_z = mag



## convert magnetometer gauss readings to compass heading
	compass = atan2(mag_y,mag_x) * (180/pi)
	wind = compass
	tilt= atan2(accel_y,accel_x) * (180/pi)
	if compass<0:
		wind +=360
	print('wind = ' + str(wind))


## trim sailwing
	if wind > 15 and wind <= 105:
		sail = 11.5 - (wind + 75) * degrees
		pwm.ChangeDutyCycle(sail)

	if wind > 105 and wind <= 180:
		sail = 2
		pwm.ChangeDutyCycle(sail)

	if wind > 180 and wind <= 255:
		sail = 11.5
		pwm.ChangeDutyCycle(sail)

	if wind > 255 and wind <= 345:
		sail = 11.5 - (wind - 255) * degrees
		pwm.ChangeDutyCycle(sail)
	print('wind: ' + str(wind))
	print('sail: ' + str(sail/degrees))

	time.sleep(.5)



