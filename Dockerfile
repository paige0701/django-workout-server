# syntax=docker/dockerfile:1
FROM python:3

RUN apt-get -y update && apt-get -y dist-upgrade
RUN apt-get install -y apt-utils dialog libpq-dev

RUN apt-get install -y python3-pip python3-dev
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE 1
# pip setuptools 업그레이드
RUN pip3 install --upgrade pip
RUN pip3 install --upgrade setuptools

RUN mkdir /src
ADD ./requirements.txt /src/

RUN pip3 install -r /src/requirements.txt

WORKDIR /src
COPY . /src
