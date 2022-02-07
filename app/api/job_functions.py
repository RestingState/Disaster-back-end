from app import Session
from app.api.planet import load_planet_coordinates
from app.api.planet import Planet as PlanetClass
import datetime
from app.models.models import Planet, PlanetCoordinates


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
