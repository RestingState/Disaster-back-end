from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from flask_bcrypt import Bcrypt
from datetime import timedelta
from flask_jwt_extended import JWTManager
import os

api = Flask(__name__)
api.config['JWT_SECRET_KEY'] = 'super-secret'
api.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
jwt = JWTManager(api)
bcrypt = Bcrypt(api)

user = 'postgres'
password = '12345678q'
server = 'localhost'
database = 'stellarly'

DB_URI = os.getenv('DB_URI', f'postgresql+psycopg2://{user}:{password}@{server}/{database}')

engine = create_engine(DB_URI)
SessionFactory = sessionmaker(bind=engine)
Session = scoped_session(SessionFactory)
Base = declarative_base()
