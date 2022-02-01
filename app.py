import datetime
from app import api
from app.rest import *
from wsgiref.simple_server import make_server
from app.rest.api import api_blueprint
from app.rest.sky_info_api import sky_blueprint
from apscheduler.schedulers.background import BackgroundScheduler
api.register_blueprint(api_blueprint)
api.register_blueprint(sky_blueprint)
session = Session()


def delete_records():
    date_to_delete = datetime.datetime.today() - datetime.timedelta(days=1)
    records = session.query(PlanetCoordinates).filter(PlanetCoordinates.date <= date_to_delete).all()
    for i in records:
        session.delete(i)
    session.commit()


# with make_server('', 5000, api) as server:
#     server.serve_forever()


if __name__ == "__main__":
    # api.run('0.0.0.0')
    # serve(api, port=5000)
    try:
        scheduler = BackgroundScheduler()
        scheduler.add_job(func=delete_records, trigger="interval", seconds = 5)
        # scheduler.add_job(func=delete_records, trigger="cron", day='1st tue', hour='13-14')
        scheduler.start()
    except AttributeError:
        print('There is no data in database')

    api.run(debug=True, port=5000)
