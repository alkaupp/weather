#!/usr/bin/env python
import json
import os
from argparse import ArgumentParser
from urllib.error import HTTPError
from urllib.parse import urlencode
from urllib.request import urlopen

API_URL = 'https://api.openweathermap.org/data/2.5/weather?'


def create_output_from_response(response):
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
    location_and_country = '%s,%s' % (args.location, args.country)
    query_params = {'q': location_and_country, 'APPID': args.api_key, 'units': 'metric'}
    return API_URL + urlencode(query_params)


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
    except HTTPError as error:
        if error.code == 404:
            print('error: Could not find location')

        if error.code == 401:
            print('API KEY is not valid')

