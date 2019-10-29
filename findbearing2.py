from math import *

lat1 = input('starting latitude?: ')
lat2 = input('ending latitude?: ')
lon1 = input('starting longitude?: ')
lon2 = input('ending longitude?: ')
x = lat2-lat1
y = lon2 - lon1

heading = atan2(y,x)
heading = heading * 180/pi
if heading <= 0:
        heading += 360
print(str(heading))

