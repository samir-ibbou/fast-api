# pull official base image
FROM python:3.10-slim

# set work directory
# WORKDIR /src
WORKDIR /app

# Ajout copy project
COPY . /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# copy requirements file
#COPY ./requirements.txt /src/requirements.txt

# install dependencies
#RUN set -eux \
#    && apk add --no-cache --virtual .build-deps build-base \
#    libressl-dev libffi-dev gcc musl-dev python3-dev \
#    postgresql-dev \
#    && pip install --upgrade pip setuptools wheel \
#    && pip install -r /src/requirements.txt \
#    && rm -rf /root/.cache/pip

RUN apt-get update -y \
    && apt-get install -y gcc libpq-dev \
    && /usr/local/bin/python -m pip install --upgrade pip \
    && pip3 install -r requirements.txt --no-cache-dir

# copy project
#COPY . /src/

# Execution
CMD gunicorn main:app -c gunicorn_config.py