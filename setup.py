from setuptools import setup

setup(
    name='weather',
    version='0.1',
    description='lol',
    packages=['weather'],
    entry_points={
        'console_scripts': ['weather = weather.weather:main']
    },
    author='Aleksi Kauppila',
    author_email='aleksi.kauppila@gmail.com'
)


