from flask import Blueprint
from app.models.schemas import *
from app.models.models import *
from app import Session
from marshmallow import ValidationError
from flask import Flask, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.api.weather import Weather


# blueprints
api_blueprint = Blueprint('api_blueprint', __name__)
sky_blueprint = Blueprint('sky_blueprint', __name__)

# additional objects
weather = Weather('')
