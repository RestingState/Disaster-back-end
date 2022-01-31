from app.models.models import KeyModel


def api_key_require(request, session, rights='user'):

    try:
        key = request.args.get('key', None)
        if not key:
            session.close()
            return {'message': 'Api key is not provided'}, 400

        db_key = session.query(KeyModel).filter_by(code=key).first()
        if not db_key:
            session.close()
            return {'message': 'Wrong api key provided'}, 400

        role = db_key.key_role

    except Exception:
        session.close()
        return {'message': 'internal server error'}, 500

    if not role:
        session.close()
        return {'message': 'Wrong api key provided'}, 400
    elif role == rights or role == 'admin':
        return None
    else:
        session.close()
        return {'message': 'Your api key is not suitable for this operation'}, 400


# key = api_key_require(request, session)
# if key:
#     return key
