import RPi.GPIO as GPIO
import time
import math

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
left = 5
straight = 7
right = 10

while True:
## setup magnetometer/accelerometer to read all
	accel, mag = lsm303.read()
  accel_x, accel_y, accel_z = accel
	mag_x, mag_y, mag_z = mag



## convert magnetometer gauss readings to compass heading
	compass = math.atan2(mag_y,mag_x) * (180/math.pi)
	heading = compass
	if compass<0:
		heading+=360
	print('compass = ' + str(heading))
## setup autopilot
	if heading < 270:
		pwm.ChangeDutyCycle(left)
	if heading > 300:
		pwm.ChangeDutyCycle(right)
	if heading < 300 and heading > 270:
		pwm.ChangeDutyCycle(straight)

	time.sleep(.5)

