
from math import *
import time
import adafruit_gps
import serial
import RPi.GPIO as GPIO





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


uart = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=3000)

# Create a GPS module instance.
gps = adafruit_gps.GPS(uart, debug=False)
# Turn on the basic GGA and RMC info (what you typically want)
gps.send_command(b'PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0')
# Set update rate to once a second in milliseconds (1hz) which is what you typically want.
gps.send_command(b'PMTK220,1000')

last_print = time.monotonic()
timer = time.monotonic()
number = 0
number2 = 0
start_route = 0
current_route = 0
corrected_route = 0
locations = {'currentlocation':{'latitude':0,'longitude':0},'previouslocation':{'latitude':0,'longitude':0}, 1:{'latitude':37.2,'longitude':-122.2}}
upwind = False
wind = 0
waypoint = 0
def sailwing(*args, **kwargs):

	global lsm303, pwm, left, straight, right, degrees, upwind, wind

	#setup magnetometer/accelerometer to read all
	accel, mag = lsm303.read()
	mag_x, mag_y, mag_z = mag
	#convert magnetometer gauss readings to compass heading
	compass = atan2(mag_y,mag_x) * (180/pi)
	wind = compass
#	tilt= atan2(accel_y,accel_x) * (180/pi)
	if compass<0:
		wind +=360
	#trim sailwing
	if wind > 15 and wind <= 105:
		sail = 11.5 - (wind + 75) * degrees
		pwm.ChangeDutyCycle(sail)
		upwind = False
	if wind > 105 and wind <= 180:
		sail = 2
		pwm.ChangeDutyCycle(sail)
		upwind = False
	if wind > 180 and wind <= 255:
		sail = 11.5
		pwm.ChangeDutyCycle(sail)
		upwind = False
	if wind > 255 and wind <= 345:
		sail = 11.5 - (wind - 255) * degrees
		pwm.ChangeDutyCycle(sail)
		upwind = False
	if wind > 345 or wind < 15:
		sail = straight
		upwind = True
	print('wind: ' + str(wind))
#	print('sail: ' + str(sail/degrees))


def compensate_drift(*args,**kwargs):
	global locations, last_print, start_route, current_route, corrected_route, upwind, wind

	# compensate for drift if there is any
	if current_route != start_route:
		if start_route < current_route:
			corrected_route = (current_route-start_route) + current_route
		if start_route > current_route:
			corrected_route = current_route - (start_route-current_route)
		if corrected_route < 0:
			corrected_route += 360
		if corrected_route > 360:
			corrected_route -= 360
		print('start_route: ' + str(start_route))
		print('corrected_route: ' + str(corrected_route))

	print('current_route: ' + str(current_route))

def next_waypoint(*args,**kwargs):
	global locations, waypoint, number2

	# if current location is less than .00006 degrees (22 feet) continue to the next waypoint
	if abs(locations['currentlocation']['latitude'] - locations[waypoint]['latitude']) < .00006 and abs(locations['currentlocation']['longitude'] - locations[waypoint]['longitude']) < .00006:
		waypoint +=1
		number2 = 0

def navigate(*args,**kwargs):
	global locations, last_print, start_route, current_route, number2, upwind, wind

	timer = last_print
	# set waypoint

	# find heading from current location to waypoint1
	x = locations[waypoint]['latitude'] - locations['currentlocation']['latitude']
	y = locations[waypoint]['longitude'] - locations['currentlocation']['longitude']
	current_route = int(atan2(y,x) *180/pi)
	if current_route <=0:
		current_route = current_route + 360

#	print('current_route: ' + str(current_route))
#	print('timer: ' + str(timer))
	if number2 < 1:
		start_route = current_route
		number2 = 1
	compensate_drift()
while True:

	gps.update()
	# Every second print out current location details if there's a fix.
	current = time.monotonic()
	if current - last_print >= 1.0:
		last_print = current
	if not gps.has_fix:
	# Try again if we don't have a fix yet.
		print('Waiting for fix...')
		sailwing()
		time.sleep(.5)
		continue
	# We have a fix! (gps.has_fix is true)

	print('=' * 40)  # Print a separator line.
	print('gps_timestamp: {}/{}/{} {:02}:{:02}:{:02}'.format(
		gps.timestamp_utc.tm_mon,
		gps.timestamp_utc.tm_mday,
		gps.timestamp_utc.tm_year,
		gps.timestamp_utc.tm_hour,
		gps.timestamp_utc.tm_min,
		gps.timestamp_utc.tm_sec))
	latitude = float('{0:.6f}'.format(gps.latitude))
	longitude = float('{0:.6f}'.format(gps.longitude))
#	print('Fix quality: {}'.format(gps.fix_quality))

#	if gps.satellites is not None:
#		print('# satellites: {}'.format(gps.satellites))

#	if gps.speed_knots is not None:
#		print('Speed: {} knots'.format(gps.speed_knots))
#	if gps.track_angle_deg is not None:
#		print('Track angle: {} degrees'.format(gps.track_angle_deg))
#	if gps.horizontal_dilution is not None:
#		print('Horizontal dilution: {}'.format(gps.horizontal_dilution))

	# update location
	if latitude != locations['currentlocation']['latitude'] or longitude != locations['currentlocation']['longitude']:
		locations['previouslocation'] = locations['currentlocation']
	# calculate current gps heading
	locations['currentlocation'] = {'latitude': latitude, 'longitude': longitude}
	currentx = locations['currentlocation']['latitude'] - locations['previouslocation']['latitude']
	currenty = locations['currentlocation']['longitude'] - locations['previouslocation']['longitude']
	heading = atan2(currenty,currentx) * 180/pi
	if heading <= 0:
		heading += 360
	print('actual heading: ' + str(heading))
	print('current location: ' + str(locations['currentlocation']))


	# log starting location
	if number < 1:
		locations[0] = {'latitude':latitude,'longitude':longitude}
		number+=1
	navigate()
	sailwing()
	print('waypoint: ' + str(waypoint) + str(locations[waypoint]))
	next_waypoint()

	time.sleep(.5)
