api_keys_dict = {'123123123': 'admin', '124124124': 'user'}


def api_key_require(request, rights='user'):
    try:
        key = request.args.get('key', None)
    except Exception:
        return {'message': 'internal server error'}, 500

    # getting key role
    role = api_keys_dict.get(key, None)

    if not role:
        return {'message': 'Wrong api key provided'}, 400
    elif role == rights or role == 'admin':
        return None
    else:
        return {'message': 'Your api key is not suitable for this operation'}, 400
