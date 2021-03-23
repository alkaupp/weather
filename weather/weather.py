import json
from http.client import HTTPResponse
from urllib.parse import urlencode
from urllib.request import urlopen


class MeasurementUnit:
    def __init__(self, name: str, temperature: str, wind_speed: str):
        self.name = name
        self.temperature = temperature
        self.wind_speed = wind_speed


class OpenWeatherMapApi:
    def __init__(self, location: str, country: str, api_key: str, unit_system: str):
        self.unit_system = unit_system
        self.api_key = api_key
        self.country = country
        self.location = location
        self.API_URL = 'https://api.openweathermap.org/data/2.5/weather?'

    def fetch(self):
        return urlopen(self.build_url())

    def build_url(self):
        location_and_country = '%s,%s' % (self.location, self.country)
        query_params = {'q': location_and_country, 'APPID': self.api_key, 'units': self.unit_system}
        return self.API_URL + urlencode(query_params)


class WeatherUpdate:
    def __init__(self, area, country, description, temperature, feels_like, wind_speed, humidity, measurement_unit: MeasurementUnit):
        self.measurement_unit = measurement_unit
        self.description = description
        self.humidity = humidity
        self.wind_speed = wind_speed
        self.feels_like = feels_like
        self.temperature = temperature
        self.country = country
        self.area = area

    @staticmethod
    def from_response(response: HTTPResponse, measurement_unit: MeasurementUnit):
        json_contents = json.loads(response.read())
        return WeatherUpdate(
            json_contents.get('name'),
            json_contents.get('sys').get('country'),
            json_contents.get('weather')[0].get('description'),
            json_contents.get('main').get('temp'),
            json_contents.get('main').get('feels_like'),
            json_contents.get('wind').get('speed'),
            json_contents.get('main').get('humidity'),
            measurement_unit
        )

    def __str__(self):
        header = '🌍 %s, %s: %s\n' % (self.area, self.country, self.description)
        return ''.join(
            [
                header,
                '-' * len(header),
                '\n🌡️  Temperature: %s %s\n' % (self.temperature, self.measurement_unit.temperature),
                '⚖️  Feels like: %s %s\n' % (self.feels_like, self.measurement_unit.temperature),
                '💦 Humidity: %s %%\n' % self.humidity,
                '🌬  Wind speed: %s %s' % (self.wind_speed, self.measurement_unit.wind_speed)
            ]
        )


class WeatherScript:
    def __init__(self, weather_api, measurement_unit: MeasurementUnit):
        self.weather_api = weather_api
        self.measurement_unit = measurement_unit

    def run(self):
        print(WeatherUpdate.from_response(self.weather_api.fetch(), self.measurement_unit))
