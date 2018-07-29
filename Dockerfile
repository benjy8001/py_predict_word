FROM debian:jessie

RUN echo "deb http://deb.debian.org/debian jessie-backports main" >> /etc/apt/sources.list
RUN echo "deb http://deb.debian.org/debian jessie non-free" >> /etc/apt/sources.list

RUN apt-get -y update && apt-get upgrade -y
RUN apt-get install -y python3 python3-dev python3-pip

RUN apt-get install -y vim build-essential 
RUN apt-get -y update && apt-get install -y calibre alsa-utils libttspico-utils

RUN mkdir /shared

COPY . /shared/

RUN python3 -m pip install pip setuptools virtualenv --upgrade

RUN mkdir -p /mnt/apps/ && \
    virtualenv -p $(which python3) /mnt/apps/predict && \
    echo "source /mnt/apps/predict/bin/activate" >> /root/.bashrc && \
    /mnt/apps/predict/bin/pip install pip setuptools --upgrade

RUN cd /shared && /mnt/apps/predict/bin/pip install --quiet -r requirements.txt
RUN cd /shared && /mnt/apps/predict/bin/python setup.py develop

COPY entrypoint.sh /entrypoint.sh
ENTRYPOINT /entrypoint.sh

ENV LANG C.UTF-8
ENV DISPLAY :0

VOLUME ["/shared"]
WORKDIR /shared