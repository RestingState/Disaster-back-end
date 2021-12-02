import requests

BASE = "https://api.n2yo.com/rest/v1/satellite/"
apiKey = 'WYY6AU-RLC84J-6AEU6S-4T6J'

def get_TLE(id):
    response = requests.get(f"{BASE}tle/{id}&apiKey={apiKey}")
    return response.json()

def get_satellite_position(id, observer_lat, observer_lng, observer_alt, seconds):
    response = requests.get(f"{BASE}positions/{id}/{observer_lat}/{observer_lng}/{observer_alt}/{seconds}/&apiKey={apiKey}")
    return response.json()