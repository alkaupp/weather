import os
import sys
from argparse import ArgumentParser
from urllib.error import HTTPError

from .weather import MeasurementUnit, WeatherScript, OpenWeatherMapApi


def build_weather_script():
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
    parser.add_argument('--imperial', action='store_true')
    args = parser.parse_args()
    units = MeasurementUnit('metric', 'C', 'm/s')
    if args.imperial:
        units = MeasurementUnit('imperial', 'F', 'miles/h')
    return WeatherScript(OpenWeatherMapApi(args.location, args.country, args.api_key, units.name), units)


def main():
    try:
        script = build_weather_script()
        script.run()
        sys.exit(0)
    except KeyError as error:
        print(
            'API key required for Open Weather Map\n'
            'You can provide it by using the --api-key=mykey flag.\n'
            'Alternatively you can export OPEN_WEATHER_MAP_API_KEY=mykey.'
        )
        sys.exit(-1)
    except HTTPError as error:
        if error.code == 404:
            print('error: Could not find location')

        if error.code == 401:
            print('API KEY is not valid')

        sys.exit(-1)
