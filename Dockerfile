# PROD CONFIG

FROM python:3.8-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./requirements/base.txt /app/requirements/base.txt

RUN python -m pip install -r /app/requirements/base.txt
