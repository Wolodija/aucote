FROM ubuntu:19.04
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    software-properties-common \
    libffi-dev \
    python3-setuptools \
    python3-pip \
    python3-dev \
    libyaml-dev \
    libpq-dev \
    curl \
    git \
    bash

ADD requirements.txt requirements.txt
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt -v
RUN pip3 install virtualenv pylint nose nose-cov bandit
