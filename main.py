import json
import os
from argparse import ArgumentParser
from urllib.request import urlopen

API_URL = 'http://api.openweathermap.org/data/2.5/weather?q=%s,%s&APPID=%s&units=metric'


def create_output_from_response(response):
    json_contents = json.loads(response.read())
    output = '%s, %s: ' % (json_contents.get('name'), json_contents.get('sys').get('country'))
    output += '%s\n' % (json_contents.get('weather')[0].get('description'))
    output += '-' * len(output)
    output += '\nTemperature: %s C\n' % json_contents.get('main').get('temp')
    output += 'Feels like: %s C\n' % json_contents.get('main').get('feels_like')
    output += 'Humidity: %s %%\n' % json_contents.get('main').get('humidity')
    output += 'Wind speed: %s' % json_contents.get('wind').get('speed')
    return output


def parse():
    parser = ArgumentParser(
        description='Get weather for a location in a country',
        usage='weather [location] [country]'
    )
    parser.add_argument('location', type=str, help='City or area')
    parser.add_argument('country', type=str, help='Country name or country code')
    parser.add_argument(
        '--api-key',
        type=str, help='API key for Open Weather Map',
        default=os.environ['OPEN_WEATHER_MAP_API_KEY']
    )
    args = parser.parse_args()
    return API_URL % (args.location, args.country, args.api_key)


if __name__ == '__main__':
    url = parse()
    response = urlopen(url)
    print(create_output_from_response(response))

