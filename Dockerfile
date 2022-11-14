FROM python:3.10-slim-buster

RUN apt update &&  \
    apt install -y imagemagick

WORKDIR /app

COPY requirements.txt ./
# COPY . .
RUN pip install -r requirements.txt
ENTRYPOINT python karate_club.py
