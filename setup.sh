#!/bin/zsh

pip install pipenv
pipenv install --python 3

pipenv run python manage.py migrate

pipenv run python manage.py collectstatic
