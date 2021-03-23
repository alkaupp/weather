#!/usr/bin/env bash
python -m venv venv
source venv/bin/activate
pip install wheel
python setup.py bdist_wheel
deactivate
pip install dist/*
rm -rf build dist weather.egg_info venv
