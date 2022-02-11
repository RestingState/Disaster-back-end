from . import subscription_blueprint
from app import Session
from flask import request
from app.models.models import user_satellite, User, Satellites
# from app.models.schemas import UserSatelliteSchema
from flask_jwt_extended import jwt_required, get_jwt_identity
# from marshmallow import ValidationError


@subscription_blueprint.route('/satellite/subscribe', methods=['POST'])
@jwt_required()
def add_satellite_subscription():
    session = Session()
    current_identity_username = get_jwt_identity()
    data = request.get_json()

    if not data or 'user_id' not in data or 'satellite_id' not in data:
        return {'message': 'Wrong input data provided'}, 400

    user = session.query(User).filter_by(username=current_identity_username).first()
    if not user:
        return {'message': 'User not found'}, 404

    if user.id != int(data['user_id']):
        return {'message': 'Access is denied'}, 403

    satellite = session.query(Satellites).filter_by(norad_id=int(data['satellite_id'])).first()
    if not satellite:
        return {'message': 'Satellite not found'}, 404

    subscription = session.query(user_satellite).filter_by(user_id=int(data['user_id']),
                                                           satellite_id=int(data['satellite_id'])).first()
    if subscription:
        return {'message': 'You are already subscribed for this satellite'}, 403

    # try:
    #     valid_data = UserSatelliteSchema().load(data)
    # except ValidationError as err:
    #     return err.messages, 422

    user.satellite.append(satellite)
    # user_satellite_object = user_satellite(**valid_data)
    session.add(user)
    session.commit()
    session.close()

    return {'message': 'Success'}