FROM python:3.6

COPY requirements.txt /requirements.txt
RUN pip3 install -r requirements.txt
RUN pip3 install bandit
RUN pip3 install nose
RUN pip3 install coverage
RUN pip3 install pylint

RUN apt-get update && apt-get install -y postgresql-client