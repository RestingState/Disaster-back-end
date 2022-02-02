from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from flask_bcrypt import Bcrypt
from datetime import timedelta
from flask_jwt_extended import JWTManager
from config import Config
from flask_cors import CORS


api = Flask(__name__)
api.config['JWT_SECRET_KEY'] = Config.JWT_SECRET_KEY
api.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=72)
jwt = JWTManager(api)
bcrypt = Bcrypt(api)
cors = CORS(api)


engine = create_engine(Config.DB_URI)
SessionFactory = sessionmaker(bind=engine)
Session = scoped_session(SessionFactory)
Base = declarative_base()
