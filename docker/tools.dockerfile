FROM python:3.8-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./requirements/tools.txt /app/requirements/tools.txt

RUN python -m pip install -r /app/requirements/tools.txt
