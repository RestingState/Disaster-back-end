from . import subscription_blueprint
from app import Session
from flask import request
from app.models.models import user_satellite, User, Satellites
from flask_jwt_extended import jwt_required, get_jwt_identity


@subscription_blueprint.route('/satellite/subscribe', methods=['POST'])
@jwt_required()
def add_satellite_subscription():
    """
    json format input:
    user_id: id of user
    satellite_id: norad_id of satellite or keyword 'all' for all of the satellites

    Creates subscription for satellites(one or all of them)
    if you call 'all' when you already have some subscriptions it will
    ignore previous and only add ones that are missing.
    """

    session = Session()
    current_identity_username = get_jwt_identity()
    data = request.get_json()

    if not data or 'user_id' not in data or 'satellite_id' not in data:
        return {'message': 'Wrong input data provided'}, 400

    try:
        if data['satellite_id'] != 'all':
            data['satellite_id'] = int(data['satellite_id'])
        data['user_id'] = int(data['user_id'])
    except ValueError:
        return {'message': 'Wrong input data provided'}, 400
    except Exception:
        return {'message': 'internal server error'}, 500

    user = session.query(User).filter_by(username=current_identity_username).first()
    if not user:
        return {'message': 'User not found'}, 404

    if user.id != data['user_id']:
        return {'message': 'Access is denied'}, 403

    if data['satellite_id'] == 'all':
        satellites = session.query(Satellites).all()
        sub_satellites = user.satellite
        for satellite in satellites:
            if satellite not in sub_satellites:
                user.satellite.append(satellite)
        session.add(user)
        session.commit()

    else:
        satellite = session.query(Satellites).filter_by(norad_id=data['satellite_id']).first()
        if not satellite:
            return {'message': 'Satellite not found'}, 404

        subscription = session.query(user_satellite).filter_by(user_id=data['user_id'],
                                                               satellite_id=data['satellite_id']).first()
        if subscription:
            return {'message': 'You are already subscribed for this satellite'}, 403

        user.satellite.append(satellite)
        session.add(user)
        session.commit()

    session.close()
    return {'message': 'Success'}


@subscription_blueprint.route('/satellite/unsubscribe', methods=['DELETE'])
@jwt_required()
def delete_satellite_subscription():
    """
    json format input:
    user_id: id of user
    satellite_id: norad_id of satellite or keyword 'all' for all of the satellites

    Deletes subscription for satellites(one or all of your subscriptions).
    """

    session = Session()
    current_identity_username = get_jwt_identity()
    data = request.get_json()

    if not data or 'user_id' not in data or 'satellite_id' not in data:
        return {'message': 'Wrong input data provided'}, 400

    try:
        if data['satellite_id'] != 'all':
            data['satellite_id'] = int(data['satellite_id'])
        data['user_id'] = int(data['user_id'])
    except ValueError:
        return {'message': 'Wrong input data provided'}, 400
    except Exception:
        return {'message': 'internal server error'}, 500

    user = session.query(User).filter_by(username=current_identity_username).first()
    if not user:
        return {'message': 'User not found'}, 404

    if user.id != data['user_id']:
        return {'message': 'Access is denied'}, 403

    if data['satellite_id'] == 'all':
        user.satellite = []
        session.add(user)
        session.commit()

    else:
        satellite = session.query(Satellites).filter_by(norad_id=data['satellite_id']).first()
        if not satellite:
            return {'message': 'Satellite not found'}, 404

        subscription = session.query(user_satellite).filter_by(user_id=data['user_id'],
                                                               satellite_id=data['satellite_id']).first()
        if not subscription:
            return {'message': 'You are not subscribed for this satellite'}, 403

        user.satellite.remove(satellite)
        session.add(user)
        session.commit()

    session.close()
    return {'message': 'Success'}
