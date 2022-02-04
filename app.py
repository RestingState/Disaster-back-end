import datetime
from app import api
from app.rest import *
from wsgiref.simple_server import make_server
from app.rest.api import api_blueprint
from app.rest.sky_info_api import sky_blueprint
from apscheduler.schedulers.background import BackgroundScheduler
from app.api.planet import load_planet_coordinates
from app.api.planet import Planet as PlanetClass


api.register_blueprint(api_blueprint)
api.register_blueprint(sky_blueprint)
session = Session()


def delete_records():
    date_to_delete = datetime.datetime.today() - datetime.timedelta(days=1)
    records = session.query(PlanetCoordinates).filter(PlanetCoordinates.date <= date_to_delete).all()
    for i in records:
        session.delete(i)
    session.commit()


def insert_records():
    planets = session.query(Planet).all()

    start_time = datetime.datetime.today()
    stop_time = datetime.datetime.today() + datetime.timedelta(days=32)

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


with make_server('', 5000, api) as server:

    # updates planet_coordinates every month at 1st day and concrete hour(example: 14:44:00)
    # deletes old planet_coordinates every month at 1st day and concrete hour(example: 14:45:00)
    try:
        scheduler = BackgroundScheduler()
        scheduler.add_job(func=insert_records, trigger="cron",
                          year='*', month='*', day=1, hour=14, minute=44, second=0)
        scheduler.add_job(func=delete_records, trigger="cron",
                          year='*', month='*', day=1, hour=14, minute=45, second=0)
        scheduler.start()
    except AttributeError:
        print('There is no data in database')
    except Exception:
        print('Internal server error')

    server.serve_forever()


# if __name__ == "__main__":
#     # api.run('0.0.0.0')
#     # serve(api, port=5000)
#     try:
#         scheduler = BackgroundScheduler()
#         # scheduler.add_job(func=delete_records, trigger="interval", seconds=60)
#         # scheduler.add_job(func=delete_records, trigger="cron", day='1st tue')
#         # scheduler.add_job(func=insert_records, trigger="interval", seconds=30)
#         # scheduler.add_job(func=insert_records, trigger="cron", second='*/10')
#         scheduler.add_job(func=insert_records, trigger="cron",
#                           year='*', month='*', day=1, hour=14, minute=39, second=0)
#         scheduler.add_job(func=delete_records, trigger="cron",
#                           year='*', month='*', day=1, hour=14, minute=39, second=30)
#         scheduler.start()
#     except AttributeError:
#         print('There is no data in database')
#
#     api.run(debug=False, port=5000)
