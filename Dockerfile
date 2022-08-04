# pull official base image
FROM python:3.9-slim-bullseye

# set work directory
WORKDIR /usr/src/prj

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY . .

RUN apt-get update && apt-get install --no-install-recommends -y \
    gcc libc-dev libpq-dev  python-dev libxml2-dev libxslt1-dev python3-lxml && apt-get install -y cron &&\
    pip install --no-cache-dir -r requirements.txt
