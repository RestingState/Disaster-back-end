from app.rest import *
from app import bcrypt


@api_blueprint.route('/user', methods=['POST'])
def create_user():
    session = Session()
    data = request.get_json()

    if data is None:
        return {'message': 'Empty input data provided'}, 400

    try:
        user_data = UserSchema().load(data)
    except ValidationError as err:
        return err.messages, 422

    user_data.update(password=bcrypt.generate_password_hash(data['password']).decode('utf-8'))
    user = User(**user_data)

    exists = session.query(User).filter_by(username=data['username']).first()
    if exists:
        return {'message': 'User with this username exists'}, 400

    exists = session.query(User).filter_by(email=data['email']).first()
    if exists:
        return {'message': 'User with this email exists'}, 400

    session.add(user)
    session.commit()
    session.close()

    return {'message': 'User successfully created'}


@api_blueprint.route('/user/login', methods=['GET'])
def login_user():
    session = Session()
    data = request.get_json()

    if not data or 'username' not in data or 'password' not in data:
        return {'message': 'Wrong input data provided'}, 401

    user = session.query(User).filter_by(username=data['username']).first()

    if user is None:
        return {'message': 'User not found'}, 404

    if not bcrypt.check_password_hash(user.password, data['password']):
        return {'message': 'Invalid username or password provided'}, 400

    access_token = create_access_token(identity=user.username)
    session.close()

    return {'token': access_token}


@api_blueprint.route('/user/<username>', methods=['GET'])
@jwt_required()
def get_user(username):
    session = Session()
    current_identity_username = get_jwt_identity()

    user = session.query(User).filter_by(username=username).first()
    if user is None:
        return {'message': 'Invalid username provided'}, 400

    if current_identity_username != username:
        return {'message': 'Access is denied'}, 403

    return jsonify(UserSchema().dump(user))
