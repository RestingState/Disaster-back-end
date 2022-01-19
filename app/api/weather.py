import json
import requests


class Weather:
    """
    Class for getting weather data.
    Uses OpenWeatherMap API.
    """

    def __init__(self, api_key):
        """Needs api_key - OpenWeatherMap API key."""
        self.api_key = api_key

    @staticmethod
    def __format_weather_data(data):
        """
        data: dict
        Returns dict of 'weather', 'clouds', 'timezone', 'name' from data
        """
        result = {}
        parameters = ['weather', 'clouds', 'timezone', 'name']
        for parameter in parameters:
            if parameter in data:
                result[parameter] = data[parameter]
        return result

    def in_the_city(self, city):
        """
        city: str
        Returns a json weather data using city.
        """
        response = requests.get(f'http://api.openweathermap.org/data/2.5/weather?'
                                f'q={city}&'
                                f'appid={self.api_key}')
        data = json.loads(response.text)
        if data['cod'] != 200:
            return data
        return self.__format_weather_data(data)

    def using_lat_and_lon(self, latitude, longitude):
        """
        latitude: str
        longitude: str
        Returns a json weather data using latitude and longitude.
        """
        response = requests.get(f'http://api.openweathermap.org/data/2.5/'
                                f'weather?'
                                f'lat={latitude}&'
                                f'lon={longitude}&'
                                f'appid={self.api_key}')
        data = json.loads(response.text)
        if data['cod'] != 200:
            return data
        return self.__format_weather_data(data)
