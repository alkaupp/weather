import os
import sys
import unittest

from .__main__ import build_weather_script
from .weather import MeasurementUnit, WeatherUpdate


class FakeResponse:
    def read(self):
        return (
            b'{"coord":{"lon":24.8458,"lat":60.2804},"weather":[{"id":803,"main":"Clouds","description":"broken '
            b'clouds","icon":"04d"}],"base":"stations","main":{"temp":2.62,"feels_like":-4.74,"temp_min":1.67,'
            b'"temp_max":3.33,"pressure":990,"humidity":69},"visibility":10000,"wind":{"speed":7.2,"deg":300},'
            b'"clouds":{"all":75},"dt":1616321312,"sys":{"type":1,"id":1332,"country":"FI","sunrise":1616300342,'
            b'"sunset":1616344589},"timezone":7200,"id":6691859,"name":"Martinlaakso","cod":200}'
        )


class ScripTestCase(unittest.TestCase):
    def setUp(self) -> None:
        sys.argv.clear()

    def test_output_is_well_formatted(self):
        self.assertEqual(
            (
                '🌍 Martinlaakso, FI: broken clouds\n'
                '----------------------------------\n'
                '🌡️  Temperature: 2.62 C\n'
                '⚖️  Feels like: -4.74 C\n'
                '💦 Humidity: 69 %\n'
                '🌬  Wind speed: 7.2 m/s'
            ),
            str(WeatherUpdate.from_response(FakeResponse(), MeasurementUnit('metric', 'C', 'm/s')))
        )

    def test_parse_args_throws_key_error(self):
        try:
            sys.argv.append('')
            sys.argv.append('boston')
            sys.argv.append('usa')
            build_weather_script()
        except KeyError as error:
            self.assertEqual('OPEN_WEATHER_MAP_API_KEY', error.args[0])

    def test_parse_args(self):
        sys.argv.append('')
        sys.argv.append('boston')
        sys.argv.append('usa')
        os.environ['OPEN_WEATHER_MAP_API_KEY'] = 'rofl'
        url = build_weather_script().weather_api.build_url()
        self.assertEqual('https://api.openweathermap.org/data/2.5/weather?q=boston%2Cusa&APPID=rofl&units=metric', url)


if __name__ == '__main__':
    unittest.main()
