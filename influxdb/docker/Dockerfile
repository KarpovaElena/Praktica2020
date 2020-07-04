FROM python:3.8
MAINTAINER KARPOVA ELENA <Bear-cub72@yandex.ru>
ENV DEBIAN_FRONTEND noninteractive
#директория для контейнера
WORKDIR /usr/src/app
#скачивание
RUN apt-get update && apt-get install -y python3-pip && pip3 install matplotlib influxdb\
    && apt-get install -y python3-tk 
COPY prog/ /usr/src/app/prog
COPY start.sh /usr/src/app
RUN chmod -x start.sh
