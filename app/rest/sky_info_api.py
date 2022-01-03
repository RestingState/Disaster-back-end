from . import sky_blueprint, weather
from app import Session
from flask import jsonify
from app.models.models import User, City
from app.models.schemas import UserSchema
from flask_jwt_extended import jwt_required, get_jwt_identity


@sky_blueprint.route('/stars/<limit>', methods=['GET'])
def get_stars_filter_by_limit(limit):
    """
    !!!WARNING!!!
    this method works with table USER because STAR isn`t created yet
    User should be replaces with Star model
    UserSchema should be replaces with Star schema

    limit: int
    Returns list of stars limited by the given integer

    Notice: if limit is greater than actual number of stars it will return all of them
    """

    session = Session()

    try:
        limit = int(limit)
    except ValueError:
        return {'message': 'Wrong input data provided'}, 400

    result = []
    stars = session.query(User).limit(limit)
    for star in stars:
        result.append(UserSchema().dump(star))

    session.close()
    return jsonify(result)


@sky_blueprint.route('/satellites/<limit>', methods=['GET'])
def get_satellites_filter_by_limit(limit):
    """
    !!!WARNING!!!
    this method works with table USER because SATELLITE isn`t created yet
    User should be replaces with Satellite model
    UserSchema should be replaces with Satellite schema

    limit: int
    Returns list of satellites limited by the given integer

    Notice: if limit is greater than actual number of satellite it will return all of them
    """

    session = Session()

    try:
        limit = int(limit)
    except ValueError:
        return {'message': 'Wrong input data provided'}, 400

    result = []
    stars = session.query(User).limit(limit)
    for star in stars:
        result.append(UserSchema().dump(star))

    session.close()
    return jsonify(result)


@sky_blueprint.route('/weather', methods=['GET'])
@jwt_required()
def get_weather_for_user():
    """
    Before using this method make sure the api key in
    app.rest.__init__ is provided for Weather class

    Returns weather for current user location.
    In case there is a trouble with api you will get 401
    """

    session = Session()
    current_identity_username = get_jwt_identity()

    user = session.query(User).filter_by(username=current_identity_username).first()
    city = session.query(City).filter_by(id=user.city_id).first()
    data = weather.in_the_city(city.name)
    return (jsonify(data), 200) if data else ({'message': 'Wrong city or api key provided'}, 401)
