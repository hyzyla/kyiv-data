FROM python:3.8-slim

EXPOSE 7070

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./requirements/prod.txt /app/requirements/prod.txt

RUN python -m pip install -r /app/requirements/prod.txt

ADD . .

CMD ["gunicorn"  , "-b", "0.0.0.0:7070", "app.main:app"]
