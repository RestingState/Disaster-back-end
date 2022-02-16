from app import Session
from app.api.planet import load_planet_coordinates
from app.api.planet import Planet as PlanetClass
import datetime
from app.models.models import *
from app.api.satellite import Satellite
from app.api.email_newsletter import send_event_email
from textwrap import wrap


def delete_records():
    session = Session()
    date_to_delete = datetime.datetime.today() - datetime.timedelta(days=1)
    records = session.query(PlanetCoordinates).filter(PlanetCoordinates.date <= date_to_delete).all()
    for i in records:
        session.delete(i)
    session.commit()
    session.close()


def insert_records():
    session = Session()
    planets = session.query(Planet).all()

    start_time = datetime.datetime.today()
    stop_time = datetime.datetime.today() + datetime.timedelta(days=32)

    # update day settings
    start_time = start_time.strftime('%Y-%m-02')
    stop_time = stop_time.strftime('%Y-%m-01')

    for planet in planets:
        try:
            coordinates = PlanetClass.get_dec_and_ra_in_time_interval(planet.name, start_time, stop_time)
        except Exception:
            print('Internal server error')
        else:
            loading_result = load_planet_coordinates(planet, coordinates, session)
            if loading_result:
                print('Internal server error')
    session.commit()
    session.close()


def check_satellite_subscription():
    session = Session()
    subscriptions = session.query(user_satellite).order_by("user_id").all()
    text = ''

    for i in range(0, len(subscriptions)):

        user = session.query(User).filter_by(id=subscriptions[i][0]).first()
        user_city = user.city_id
        city = session.query(City).filter_by(id=user_city).first()
        latitude = float(city.latitude)
        longitude = float(city.longitude)
        user_email = user.email

        satellite = session.query(Satellites).filter_by(norad_id=subscriptions[i][1]).first()
        data_satellite = '2 ' + str(satellite.norad_id) + ' ' + \
                         satellite.ascending_node_longitude + ' ' + \
                         satellite.eccentricity + ' ' + \
                         satellite.pericenter_argument + ' ' + \
                         satellite.average_anomaly + ' ' + \
                         satellite.inclination + ' ' + \
                         satellite.call_frequency

        sat = Satellite(satellite.norad_id)

        message = Satellite.get_satellite_observation(sat, data_satellite, latitude, longitude)
        message = message[:-1]
        message = message.split(' ')
        message = [' '.join(x) for x in zip(message[0::2], message[1::2])]
        message = '\n'.join(message)

        if message != 'No observation of satellite soon':
            if (i == len(subscriptions) - 1) or (i != len(subscriptions) - 1 and subscriptions[i][0] != subscriptions[i + 1][0]):
                text += f'Satellite \'{satellite.satname}\' with norad \'{satellite.norad_id}\' can be ' \
                        f'observed at:\n{message}\n'
                send_event_email(user.first_name + ' ' + user.last_name, user_email, 'Future satellites flights', city.name, text)
                text = ''
            elif subscriptions[i][0] == subscriptions[i + 1][0] and i != len(subscriptions) - 1:
                text += f'Satellite \'{satellite.satname}\' with norad \'{satellite.norad_id}\' can be ' \
                        f'observed at:\n{message}\n'
