import os


user = os.environ.get('STELLARLY_USER')
password = os.environ.get('STELLARLY_PASSWORD')
server = os.environ.get('STELLARLY_SERVER')
database = 'stellarly'


class Config:
    """
    Provides configuration settings and api keys.
    """

    DB_URI = os.getenv('DB_URI', f'postgresql://jwybdxdlrzhdqo:43dbc041a5cdd9494c373cc1ba1a74dfb0e06bd0b35783472cf8a2c0d5f471a2@ec2-54-78-36-245.eu-west-1.compute.amazonaws.com:5432/dcdois4sl8pdd2')
    JWT_SECRET_KEY = 'super-secret'
    WEATHER_API_KEY = '38a998fffca4ade707ae1065880997a3'
    ADMIN_PASSWORD = '8Gaw$S@6Paq%rRC'



