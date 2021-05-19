FROM python:3.8.10
LABEL maintainer="jameelhamdan99@yahoo.com"
COPY requirements.txt /
RUN pip install -U pip && pip install -r requirements.txt && pip install -r requirements-extra.txt
WORKDIR /usr/src/app
COPY . .
RUN chmod -R 777 .
