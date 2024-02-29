FROM python:3.11.8-slim

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1

ENV PYTHONUNBUFFERED 1

RUN apt-get update && \
    apt-get -y install netcat-traditional gcc && \
    apt-get -y install libpq-dev gcc && \
    apt-get clean

RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
