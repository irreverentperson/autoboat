
from math import *
import time
import adafruit_gps
import serial
import RPi.GPIO as GPIO

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
locations = {'currentlocation':{'latitude':0,'longitude':0},'previouslocation':{'latitude':0,'longitude':0}}
def compensate_drift(*args,**kwargs):
	global locations
	global last_print
	global start_route
	global current_route
	global corrected_route

	# comensate for drift if there is any
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
		print('current_route: ' + str(current_route))
		print('corrected_route: ' + str(corrected_route))
def navigate(*args,**kwargs):

	global locations
	global last_print
	global start_route
	global current_route
	global number2

	timer = last_print
	# set waypoint
	locations['waypoint1'] = {'latitude': 37.4632,'longitude': -122.4269}
	# find heading from current location to waypoint1
	x = locations['waypoint1']['latitude'] - locations['currentlocation']['latitude']
	y = locations['waypoint1']['longitude'] - locations['currentlocation']['longitude']
	current_route = int(atan2(y,x) *180/pi)
	if current_route <=0:
		current_route = current_route + 360

#	print('current_route: ' + str(current_route))
	print('timer: ' + str(timer))
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
		time.sleep(1)
		continue
	# We have a fix! (gps.has_fix is true)

	print('=' * 40)  # Print a separator line.
	print('Fix timestamp: {}/{}/{} {:02}:{:02}:{:02}'.format(
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
	print('heading: ' + str(heading))
#	print('current location: ' + str(locations['currentlocation']))
#	print('previous location: ' + str(locations['previouslocation']))
	print('locations{}: ' + str(locations))

	# log starting location
	if number < 1:
		locations['start'] = {'latitude':latitude,'longitude':longitude}
		number+=1
	navigate()
	time.sleep(.5)
