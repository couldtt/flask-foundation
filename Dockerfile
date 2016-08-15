FROM python:3.5
MAINTAINER zhangteng<fuyunbiyi@gmail.com>
ENV PYTHONUNBUFFERED 1
ENV REDIS_TCP_ADDR redis
ENV CACHE_ENV_HOST redis
ENV DB_ENV_HOST db
RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
RUN pip3 install -r requirements.txt
ADD . /code/
