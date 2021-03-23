from setuptools import setup

setup(
    name='weather',
    version='0.1',
    description='CLI frontend for querying weather',
    packages=['weather'],
    entry_points={
        'console_scripts': ['weather = weather.__main__:main']
    },
    author='Aleksi Kauppila',
    author_email='aleksi.kauppila@gmail.com'
)


