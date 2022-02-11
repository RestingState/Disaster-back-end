import os


user = os.environ.get('STELLARLY_USER')
password = os.environ.get('STELLARLY_PASSWORD')
server = os.environ.get('STELLARLY_SERVER')
database = 'stellarly'


class Config:
    """
    Provides configuration settings and api keys.
    """

    DB_URI = os.getenv('DB_URI', f'postgresql+psycopg2://{user}:{password}@{server}/{database}')
    JWT_SECRET_KEY = 'super-secret'
    WEATHER_API_KEY = '38a998fffca4ade707ae1065880997a3'
    ADMIN_PASSWORD = '8Gaw$S@6Paq%rRC'
