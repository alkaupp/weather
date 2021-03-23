import json
import os
from argparse import ArgumentParser
from urllib.parse import urlencode
from urllib.request import urlopen


class MeasurementUnit:
    def __init__(self, name: str, temperature: str, wind_speed: str):
        self.name = name
        self.temperature = temperature
        self.wind_speed = wind_speed


class WeatherScript:
    def __init__(self, location: str, country: str, api_key: str, measurement_unit: MeasurementUnit):
        self.measurement_unit = measurement_unit
        self.api_key = api_key
        self.country = country
        self.location = location
        self.API_URL = 'https://api.openweathermap.org/data/2.5/weather?'

    def run(self):
        print(self.create_output_from_response(urlopen(self.build_url()).read()))

    def create_output_from_response(self, response):
        json_contents = json.loads(response)
        header = '🌍 %s, %s: %s\n' % (
            json_contents.get('name'),
            json_contents.get('sys').get('country'),
            json_contents.get('weather')[0].get('description')
        )
        return ''.join(
            [
                header,
                '-' * len(header),
                '\n🌡️  Temperature: %s %s\n' % (json_contents.get('main').get('temp'), self.measurement_unit.temperature),
                '⚖️  Feels like: %s %s\n' % (json_contents.get('main').get('feels_like'), self.measurement_unit.temperature),
                '💦 Humidity: %s %%\n' % json_contents.get('main').get('humidity'),
                '🌬  Wind speed: %s %s' % (json_contents.get('wind').get('speed'), self.measurement_unit.wind_speed)
            ]
        )

    def build_url(self):
        location_and_country = '%s,%s' % (self.location, self.country)
        query_params = {'q': location_and_country, 'APPID': self.api_key, 'units': self.measurement_unit.name}
        return self.API_URL + urlencode(query_params)

