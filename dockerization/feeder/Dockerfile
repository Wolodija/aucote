FROM python:3.6
ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /opt/feeder

COPY ./dockerization/feeder/src ./src/
COPY ./dockerization/feeder/files/hosts_example.yml ./src/files/
COPY ./dockerization/feeder/files/entrypoint.sh /
RUN pip3 install -r ./src/requirements.txt

CMD ["/entrypoint.sh"]
