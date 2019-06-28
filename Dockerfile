FROM python:3.7

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ADD requirements.txt /
RUN pip install -r requirements.txt

COPY . /code
WORKDIR /code
