FROM python:3.7-slim-buster

RUN apt-get update && apt-get install -y build-essential python3-dev swig libssl-dev
WORKDIR /home/app/
COPY ./ /home/app/

RUN pip install pipenv && pipenv install --deploy --system

RUN python /home/app/manage.py collectstatic --no-input
