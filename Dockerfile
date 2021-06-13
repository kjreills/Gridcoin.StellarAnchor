FROM python:3.7-slim-buster

RUN apt-get update && apt-get install -y build-essential python3-dev swig libssl-dev
WORKDIR /home
RUN mkdir /home/data
COPY ./ /home/app/
COPY .env /home/

RUN pip install pipenv && pipenv install --system
