from math import *

lat1 = 0
lon1 = 0
lat2 = 0
lon2 = 0

def findheading(*args, **kwargs):
        global lat1
        global lon1
        global lat2
        global lon2

        x = sin(lon2-lon1)* cos(lat2)
        y = cos(lat1) * sin(lat2) - sin(lat1) * cos(lat2) * cos(lon2-lon1)
        bearing = atan2(x,y)
        bearing = degrees(bearing)


        if bearing < 0:
                bearing= bearing + 360

        print(str(bearing) + ' degrees')


def inputs(*args, **kwargs):
        global lat1
        global lon1
        global lat2
        global lon2

        lat1 = input('starting latitude?')
        lon1 = input('starting longitude?')
        lat2 = input('ending latitude?')
        lon2 = input('ending longitude?')
#       lat1 =float(37.1)
#       lon1 = float(-121.5)
#       lat2 = float(37.1)
#       lon2 = float(-121.1)
        findheading()

inputs()
