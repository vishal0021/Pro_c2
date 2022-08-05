from skyfield.api import load, wgs84

stations_url = 'http://celestrak.com/NORAD/elements/active.txt'
satellites = load.tle_file(stations_url,reload=True)
print('Loaded', len(satellites), 'satellites')

for i in satellites:
  print(i)

by_name = {sat.name: sat for sat in satellites}
satellite = by_name['SPACEBEE-136']
print(satellite)

"""by number"""

by_number = {sat.model.satnum: sat for sat in satellites}
satellite = by_number[52164]
print(satellite)

# Printing all the details about the satellite
#1 NORAD ID and Name

norad_id=satellite.model.satnum
print("NORAD ID: ",norad_id)
name=satellite.name
print("SATELLITE NAME: ",name)

#2 UTC Time

utc_time=satellite.epoch.utc_jpl()
print("UTC TIME: ")
print(utc_time)

#3. Local Time

import datetime
TimeDelta = datetime.timedelta(hours=5,minutes=30)
TZObject = datetime.timezone(TimeDelta,name="IST")
print("LOCAL TIME: ")
local_time=satellite.epoch.astimezone(TZObject)
print(local_time)

#4. LATITUDE, LONGITUDE"""
ts = load.timescale()
t=ts.now()
geocentric = satellite.at(t)
# print(geocentric.position.km) #returns the Cartesian x,y,z coordinates

lat, lon = wgs84.latlon_of(geocentric)
print('LATITUDE:', lat)
print('LONGITUDE:', lon)

#5. SPEED

speed=geocentric.speed()
print("SPEED: ",speed)
print(geocentric.velocity.km_per_s)

#6. AZIMUTH , ALTITUDE, DISTANCE FROM A SPECIFIC POINT ON EARTH

# importing geopy library
from geopy.geocoders import Nominatim
# calling the Nominatim tool
loc = Nominatim(user_agent="GetLoc")
# entering the location name
getLoc = loc.geocode("Mumbai")
print("MY LOCATION: ")
# printing address
print(getLoc.address)
# printing latitude and longitude
mylat=getLoc.latitude
mylong=getLoc.longitude
print("Latitude = ",mylat)
print("Longitude = ", mylong)

myloc=wgs84.latlon(mylat, mylong)

difference = satellite - myloc

topocentric = difference.at(t)
# print(topocentric.position.km)

alt, az, distance = topocentric.altaz()

if alt.degrees > 0:
    print('The ISS is above the horizon')
print('\n')
print('ELEVATION:', alt)
print('AZIMUTH:', az)
print('DISTANCE: {:.1f} km'.format(distance.km))

"""7. ELEVATION/ALTITUDE"""

pos=wgs84.geographic_position_of(geocentric)
print("ALTITUDE: ",pos.elevation.km)

"""8. RIGHT ASCENSION
9. DECLINATION
"""

ra, dec, distance = topocentric.radec()
print("RIGHT ASCENSION: ",ra)
print("DECLINATION: ",dec.degrees)
print("DISTANCE: ",distance.km)

"""10. SATELLITE IN DAY LIGHT OR NOT"""

eph = load('de421.bsp')
sunlit=satellite.at(t).is_sunlit(eph)
if (sunlit == False):
  print("Satellite is in shadow")
else:
  print("Satellite is in sun light")

