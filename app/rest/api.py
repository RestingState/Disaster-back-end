from app.rest import *
from app import bcrypt


@api_blueprint.route('/user', methods=['POST'])
def create_user():
    """

    Creates user with parameters and returns JWT token
    generated on username

    Notice: user with username 'admin' cannot be created
    because admin has special rights and cannot be added to a database
    """
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

    if data['username'] == 'admin':
        return {'message': 'Cannot create a user with \'admin\' username'}, 403

    exists = session.query(User).filter_by(username=data['username']).first()
    if exists:
        return {'message': 'User with this username exists'}, 400

    exists = session.query(User).filter_by(email=data['email']).first()
    if exists:
        return {'message': 'User with this email exists'}, 400

    session.add(user)
    session.commit()
    access_token = create_access_token(identity=user.username)
    session.close()

    return {'token': access_token}


@api_blueprint.route('/user/login', methods=['POST'])
def login_user():
    """
    Takes login:password in a Basic-authentication format

    If credentials are correct, returns JWT token
    generated on username

    Notice: if username is 'admin' and password is ADMIN_PASSWORD from config,
    returns admin JWT token
    """
    session = Session()
    data = request.get_json()

    if not data or 'username' not in data or 'password' not in data:
        return {'message': 'Wrong input data provided'}, 401

    if data['username'] == 'admin' and data['password'] == Config.ADMIN_PASSWORD:
        access_token = create_access_token(identity='admin')
        session.close()

        return {'token': access_token}

    user = session.query(User).filter_by(username=data['username']).first()

    if user is None:
        return {'message': 'User not found'}, 404

    if not bcrypt.check_password_hash(user.password, data['password']):
        return {'message': 'Invalid username or password provided'}, 400

    access_token = create_access_token(identity=user.username)
    session.close()

    return {'token': access_token}


@api_blueprint.route('/user', methods=['GET'])
@jwt_required()
def get_user():
    """
    Takes login:password in a Basic-authentication format

    If credentials are correct, returns JWT token
    generated on username

    Notice: if username is 'admin' and password is ADMIN_PASSWORD from config,
    returns admin JWT token
    """
    session = Session()
    current_identity_username = get_jwt_identity()

    user = session.query(User).filter_by(username=current_identity_username).first()
    if user is None:
        return {'message': 'Invalid token provided'}, 400

    return jsonify(UserSchema().dump(user))


@api_blueprint.route('/category', methods=['POST'])
@jwt_required()
def create_category():
    """
    Takes name of a new category

    Returns a success message

    Notice: only admin can create categories,
    so you need to provide admin JWT token
    """
    session = Session()
    current_identity_username = get_jwt_identity()
    data = request.get_json()

    if current_identity_username != 'admin':
        return {'message': 'Access is denied'}, 403

    if not data or 'name' not in data:
        return {'message': 'Wrong input data provided'}, 401

    if session.query(Category).filter_by(name=data['name']).first() is not None:
        return {'message': 'Category with this name already exists'}, 403

    category = Category(**data)
    session.add(category)
    session.commit()
    session.close()

    return {'message': 'Category is successfuly created'}, 200


@api_blueprint.route('/user/subscription', methods=['POST'])
@jwt_required()
def add_subscription():
    """
    Takes user_id and category_id

    Creates a subscription to a category and
    adds it to a database
    """
    session = Session()
    current_identity_username = get_jwt_identity()
    data = request.get_json()

    user = session.query(User).filter_by(username=current_identity_username).first()
    if user is None:
        return {'message': 'Invalid token provided'}, 400

    if not data or 'user_id' not in data or 'category_id' not in data:
        return {'message': 'Wrong input data provided'}, 401

    if user.id != int(data['user_id']):
        return {'message': 'Access is denied'}, 403

    category = session.query(Category).filter_by(id=data['category_id']).first()
    if category is None:
        return {'message': 'Category with this id does not exist'}, 400

    if session.query(user_category).filter_by(user_id=data['user_id'],
                                              category_id=data['category_id']).first() is not None:
        return {'message': 'Subscription to this category already exists'}, 403

    user.categories.append(category)
    session.add(user)
    session.commit()
    session.close()

    return {'message': 'Subscription is successfuly created'}, 200
