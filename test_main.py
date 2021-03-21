import unittest
from main import create_output_from_response


class ScripTestCase(unittest.TestCase):
    def test_output_is_well_formatted(self):
        response = (
            b'{"coord":{"lon":24.8458,"lat":60.2804},"weather":[{"id":803,"main":"Clouds","description":"broken '
            b'clouds","icon":"04d"}],"base":"stations","main":{"temp":2.62,"feels_like":-4.74,"temp_min":1.67,'
            b'"temp_max":3.33,"pressure":990,"humidity":69},"visibility":10000,"wind":{"speed":7.2,"deg":300},'
            b'"clouds":{"all":75},"dt":1616321312,"sys":{"type":1,"id":1332,"country":"FI","sunrise":1616300342,'
            b'"sunset":1616344589},"timezone":7200,"id":6691859,"name":"Martinlaakso","cod":200}'
        )
        output = (
            'Martinlaakso, FI: broken clouds\n'
            '--------------------------------\n'
            '🌡️  Temperature: 2.62 C\n'
            '⚖️  Feels like: -4.74 C\n'
            '💦 Humidity: 69 %\n'
            '🌬  Wind speed: 7.2 m/s'
        )
        self.assertEqual(output, create_output_from_response(response))


if __name__ == '__main__':
    unittest.main()
