#!/usr/bin/env python
import json
import os
from argparse import ArgumentParser
from urllib.request import urlopen

API_URL = 'https://api.openweathermap.org/data/2.5/weather?q=%s,%s&APPID=%s&units=metric'


def create_output_from_response(response):
    json_contents = json.loads(response)
    header = '%s, %s: %s\n' % (
        json_contents.get('name'),
        json_contents.get('sys').get('country'),
        json_contents.get('weather')[0].get('description')
    )
    return ''.join(
        [
            header,
            '-' * len(header),
            '\n🌡️  Temperature: %s C\n' % json_contents.get('main').get('temp'),
            '⚖️  Feels like: %s C\n' % json_contents.get('main').get('feels_like'),
            '💦 Humidity: %s %%\n' % json_contents.get('main').get('humidity'),
            '🌬  Wind speed: %s m/s' % json_contents.get('wind').get('speed')
        ]
    )


def parse_args_for_url():
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
    try:
        url = parse_args_for_url()
        response = urlopen(url)
        print(create_output_from_response(response.read()))
    except KeyError as error:
        print(
            'API key required for Open Weather Map\n'
            'You can provide it by using the --api-key=mykey flag.\n'
            'Alternatively you can export OPEN_WEATHER_MAP_API_KEY=mykey.'
        )
