import os


user = os.environ.get('STELLARLY_USER')
password = os.environ.get('STELLARLY_PASSWORD')
server = os.environ.get('STELLARLY_SERVER')
database = 'stellarly'


class Config:
    """
    Provides configuration settings and api keys.
    """

    DB_URI = os.getenv('DB_URI', f'postgresql://lwkfonojrimaki:b436bfc22e113b3f8b014e65647db47d4d225521576ec1577e36d8a002625c13@ec2-52-215-225-178.eu-west-1.compute.amazonaws.com:5432/dhvqkklauljc4')
    JWT_SECRET_KEY = 'super-secret'
    WEATHER_API_KEY = '38a998fffca4ade707ae1065880997a3'
    ADMIN_PASSWORD = '8Gaw$S@6Paq%rRC'

