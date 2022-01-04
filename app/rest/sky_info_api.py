from . import sky_blueprint, weather
from app import Session
from flask import jsonify, request
from app.models.models import User, City
from app.models.schemas import UserSchema
from flask_jwt_extended import jwt_required, get_jwt_identity


@sky_blueprint.route('/stars', methods=['GET'])
def get_stars_filter_by_limit():
    """
    !!!WARNING!!!
    this method works with table USER because STAR isn`t created yet
    User should be replaces with Star model
    UserSchema should be replaces with Star schema

    ?limit=Value: int, Default=100

    Returns list of stars limited by the given integer

    Notice: if limit is greater than actual number of stars it will return all of them
    """

    session = Session()

    limit = request.args.get('limit', 100)
    try:
        limit = int(limit)
    except ValueError:
        return {'message': 'Wrong input data provided'}, 400

    if limit < 0:
        return {'message': 'Wrong input data provided'}, 400

    result = []
    stars = session.query(User).limit(limit)
    for star in stars:
        result.append(UserSchema().dump(star))

    session.close()
    return jsonify(result)


@sky_blueprint.route('/satellites', methods=['GET'])
def get_satellites_filter_by_limit():
    """
    !!!WARNING!!!
    this method works with table USER because SATELLITE isn`t created yet
    User should be replaces with Satellite model
    UserSchema should be replaces with Satellite schema

    ?limit=Value: int, Default=100

    Returns list of satellites limited by the given integer

    Notice: if limit is greater than actual number of satellite it will return all of them
    """

    session = Session()

    limit = request.args.get('limit', 100)
    try:
        limit = int(limit)
    except ValueError:
        return {'message': 'Wrong input data provided'}, 400

    if limit < 0:
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

    ?city=Value: str, Default=user`s location

    Returns current weather for the city.
    In case there is a trouble with city you will get 401

    Notice: all the api errors including api key errors return the same
    message and code as the city error
    """

    session = Session()
    current_identity_username = get_jwt_identity()

    user = session.query(User).filter_by(username=current_identity_username).first()
    city_object = session.query(City).filter_by(id=user.city_id).first()

    city = request.args.get('city', city_object.name)

    data = weather.in_the_city(city)
    return (jsonify(data), 200) if data else ({'message': 'Wrong city provided'}, 401)
