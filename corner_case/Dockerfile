FROM python:3.8.3-slim-buster

ENV corner_case=/home/app/corner_case

RUN mkdir -p $corner_case
RUN mkdir -p $corner_case/static
COPY requirements.txt /requirements.txt
WORKDIR $corner_case

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update \
    && apt-get -y install libpq-dev gcc \
    && pip install --upgrade pip \
    && pip install psycopg2 \
    && pip install -r /requirements.txt

COPY . $corner_case