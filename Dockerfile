FROM python:3.7-slim-buster

RUN apt-get update && apt-get install -y build-essential python3-dev swig libssl-dev
WORKDIR /home
RUN mkdir /home/data
COPY app /home/app/
COPY .env requirements.txt /home/

RUN pip install -r requirements.txt && python /home/app/manage.py collectstatic --no-input

CMD python /home/app/manage.py migrate; python /home/app/manage.py runserver --nostatic 0.0.0.0:8000
#CMD echo hello world