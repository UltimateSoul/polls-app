FROM python:3.9-alpine
MAINTAINER Demid Siedykh

ENV PYTHONUNBUFFERED 1
WORKDIR /app
COPY ./requirements.txt /requirements.txt
RUN apk update && apk add bash
RUN apk add --no-cache jpeg-dev zlib-dev
RUN apk add --no-cache --virtual .build-deps build-base linux-headers
RUN apk add --update --no-cache postgresql-client
RUN apk add --update --no-cache --virtual .tmp-build-deps \
        gcc libc-dev linux-headers postgresql-dev
RUN pip install -r /requirements.txt
COPY ./backend /app
