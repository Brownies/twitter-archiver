FROM ubuntu:20.04

COPY requirements.txt docker-entrypoint.sh /

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    firefox \
    firefox-geckodriver \
    python3 \
    python3-pip \
    sqlite3 \
    xvfb \
    && pip3 install --no-cache-dir -r /requirements.txt

COPY /src /twitter-archiver

ENTRYPOINT [ "/docker-entrypoint.sh" ]
