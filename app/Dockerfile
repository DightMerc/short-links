# syntax = docker/dockerfile:experimental
FROM python:3.8.3-alpine

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install psycopg2 dependencies
RUN apk update \
    && apk add gcc python3-dev musl-dev linux-headers libc-dev mariadb-dev

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt
# RUN --mount=type=cache,target=/root/.cache/pip pip install -r requirements.txt

# copy entrypoint.sh
COPY ./entrypoint.sh .
# COPY ./create_user.sh .


# copy project
COPY . .

# run entrypoint.shentrypoint
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
# ENTRYPOINT ["/usr/src/app/create_user.sh"]

