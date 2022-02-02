import requests


class SpaceFlightsNews:
    def __init__(self):
        self.url = 'https://api.spaceflightnewsapi.net/v3/'

    def get_articles(self, count):
        try:
            response = requests.get(self.url + 'articles?_limit=' + str(count))
            return response.json()
        except ValueError:
            return "It`s not a number."

    def get_blogs(self, count):
        try:
            response = requests.get(self.url + 'blogs?_limit=' + str(count))
            return response.json()
        except ValueError:
            return "It`s not a number."

    def get_reports(self, count):
        try:
            response = requests.get(self.url + 'reports?_limit=' + str(count))
            return response.json()
        except ValueError:
            return "It`s not a number."

