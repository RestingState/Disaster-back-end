import numpy as np
from skyfield import api
from skyfield.api import load, wgs84, EarthSatellite
from datetime import datetime, timedelta
import requests

api_key = 'WYY6AU-RLC84J-6AEU6S-4T6J'  # N2YO.COM REST API v1 key


class Observer:
    """
    Class for getting Observer data.
    """

    def __init__(self,  observer_lat, observer_lng, observer_alt):
        """
        Observer's coordinates location.
        observer_lat: Observer's latitude
        observer_lng: Observer's longitude
        observer_alt: Observer's altitude
        """
        self.observer_lat = observer_lat
        self.observer_lng = observer_lng
        self.observer_alt = observer_alt

    def get_observer_coord(self):
        return self.observer_lat, \
               self.observer_lng, \
               self.observer_alt


class Satellite:
    """
    Class for getting satellites data.
    Uses N2YO.COM REST API v1.
    Uses Skyfield API
    """

    def __init__(self, sat_id):
        """
        id represents NORAD number from NORAD Catalog Number.
        NORAD Catalog: https://in-the-sky.org/search.php?s=&searchtype=Spacecraft&satorder=0

        :param sat_id: NORAD number from NORAD Catalog Number
        """
        self.id = sat_id

    def get_TLE(self):
        """
        A two-line element set (TLE) is a data format encoding a list of orbital elements
        of an Earth-orbiting object for a given point in time, the epoch.

        Uses N2YO.COM REST API v1.

        :return: json data
        """
        response = requests.get(f"https://api.n2yo.com/rest/v1/satellite/tle/{self.id}&apiKey={api_key}")

        return response.json()

    def get_satellite_position(self, observer_lat, observer_lng, observer_alt, seconds):
        """
        Retrieve the future positions of any satellite
        as footprints (latitude, longitude) to display orbits on maps.
        (Kepler orbital elements of the satellite).

        Uses N2YO.COM REST API v1.

        id: NORAD number from NORAD Catalog Number.
        observer_lat: Observer's latitude
        observer_lng: Observer's longitude
        observer_alt: Observer's altitude
        seconds: number of future positions to return. Each second is a position. Limit 300 seconds.

        :param observer_alt: int
        :param observer_lng: int
        :param observer_lat: int
        :param seconds: int
        :return: json data
        """
        response = requests.get(f"https://api.n2yo.com/rest/v1/satellite/positions/{self.id}/{observer_lat}/"
                                f"{observer_lng}/{observer_alt}/{seconds}/&apiKey={api_key}")
        return response.json()

    def get_satellite_lon_lat(self, tle, date_time_str):
        """
        Calculate longitude, latitude and elevation of a satellite's ECI coordinates
        considering Earth flattening.

        Uses Skyfield API

        tle: satellite's TLE data
        date_time_str: current/future date

        :param tle: string
        :param date_time_str: string('DD/MM/YY HH:MM:SS', day/month/year hour:minute:second, 25/01/22 11:39:19)
        :return: ECI satellite's coordinates: latitude(in degrees), longitude(in degrees), elevation(in km)
        """

        ts = load.timescale()
        date_time_obj = datetime.strptime(date_time_str, '%d/%m/%y %H:%M:%S')
        t = ts.utc(date_time_obj.year, date_time_obj.month, date_time_obj.day,
                   date_time_obj.hour, date_time_obj.minute, date_time_obj.second)

        tle = str(tle).split()
        line = tle[tle.index(f'{self.id}')-1:len(tle)]
        line2 = ""
        for ele in line:
            line2 += ele

        satellite = EarthSatellite(' ', line2, ' ', ts)
        geocentric = satellite.at(t)

        lat_lon = wgs84.geographic_position_of(geocentric)
        lat_lon = str(lat_lon).split()
        lat, lon = float(lat_lon[2]), float(lat_lon[5])
        elev = wgs84.height_of(geocentric).km

        return lat, lon, elev

    def get_observe_satellite(self, tle, date_time_str, observer_lat, observer_lon):
        """
        Calculate satellite altitude, azimuth, and distance relative to an observer.

        Uses Skyfield API

        tle: satellite's TLE data
        date_time_str: current/future date
        observer_lat: Observer's latitude
        observer_lon: Observer's longitude

        :param tle: string
        :param date_time_str: string('DD/MM/YY HH:MM:SS', day/month/year hour:minute:second, 25/01/22 11:39:19)
        :param observer_lat: float
        :param observer_lon: float
        :return: satellite altitude(in degrees), azimuth(in degrees), and distance(in km) relative to an observer
        """

        ts = load.timescale()
        date_time_obj = datetime.strptime(date_time_str, '%d/%m/%y %H:%M:%S')
        t = ts.utc(date_time_obj.year, date_time_obj.month, date_time_obj.day,
                   date_time_obj.hour, date_time_obj.minute, date_time_obj.second)

        tle = str(tle).split()
        line = tle[tle.index(f'{self.id}')-1:len(tle)]
        line2 = ""
        for ele in line:
            line2 += ele

        satellite = EarthSatellite(' ', line2, ' ', ts)

        observer = wgs84.latlon(observer_lat, observer_lon)

        difference = satellite - observer
        centric = difference.at(t)
        alt, az, distance = centric.altaz()

        if alt.degrees > 0:
            print('The ISS is above the horizon')

        return alt.degrees, az.degrees, distance.km

    def get_satellite_observation(self, tle, observer_lat, observer_lon):
        """
        Calculate satellite passes through 2 days relative to an observer.

        Uses Skyfield API

        tle: satellite's TLE data
        observer_lat: Observer's latitude
        observer_lon: Observer's longitude

        :param tle: string
        :param observer_lat: float
        :param observer_lon: float
        :return: satellite passes relative to an observer
        """

        # two day, starting at datetime.now UTC
        dateTimeObj = datetime.now()
        minutes = range(60 * 24 * 2)
        ts = api.load.timescale()
        t = ts.utc(int(dateTimeObj.year), int(dateTimeObj.month), int(dateTimeObj.day),
                   int(dateTimeObj.hour), minutes)

        tle = str(tle).split()
        line = tle[tle.index(f'{self.id}')-1:len(tle)]
        line2 = ""
        for ele in line:
            line2 += ele

        satellite = EarthSatellite(' ', line2, ' ', ts)

        observer = api.Topos(observer_lat, observer_lon)

        difference = satellite - observer
        centric = difference.at(t)
        alt, az, distance = centric.altaz()

        above_horizon = alt.degrees > 0
        # indicators, = above_horizon.nonzero()

        boundaries, = np.diff(above_horizon).nonzero()

        if np.size(boundaries) > 1:
            passes = boundaries.reshape(len(boundaries) // 2, 2)
            result = []
            for k in range(np.size(passes) - 1):
                i, j = passes[k]
                result.append('Rises above the horizon: ' + str(datetime.now() + timedelta(minutes=int(i))) +
                              ' Sets below the horizon: ' + str(datetime.now() + timedelta(minutes=int(j))))
            return result
        elif np.size(boundaries) == 1:
            return str(datetime.now() + timedelta(minutes=int(boundaries[0])))
        else:
            return "No observation of satellite soon"

# EXAMPLE
# sat = Satellite(25544)
# date_time = '21/01/22 11:39:19'
# tle_ = "1 25544U 98067A   18077.09047010  .00001878  00000-0  35621-4 0  9999 " \
#       "2 25544  51.6412 112.8495 0001928 208.4187 178.9720 15.54106440104358"
# print(sat.get_satellite_lon_lat(tle_, date_time))
