import requests

apiKey = 'WYY6AU-RLC84J-6AEU6S-4T6J'

def get_TLE(id):
    response = requests.\
        get("https://api.n2yo.com/rest/v1/satellite/tle/{}&apiKey={}"\
        .format(id, apiKey))
    return response.json()

def get_satellite_position(id, observer_lat, observer_lng, observer_alt, seconds):
    response = requests.\
        get("https://api.n2yo.com/rest/v1/satellite/positions/{}/{}/{}/{}/{}/&apiKey={}"\
        .format(id, observer_lat, observer_lng, observer_alt, seconds, apiKey))
    return response.json()

print(get_TLE(25544))
print(get_satellite_position(25544, 41.702, -76.014, 0, 2))