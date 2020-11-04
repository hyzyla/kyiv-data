FROM python:3.8-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./requirements/prod.txt /app/requirements/prod.txt

RUN python -m pip install -r /app/requirements/prod.txt

EXPOSE 8000

CMD ["gunicorn"  , "-b", "0.0.0.0:8000", "app:main"]
