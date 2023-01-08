# Base

FROM python:3.11-slim

# Dependencies

COPY requirements.txt ./
RUN apt update > /dev/null && \
        apt install -y build-essential && \
        pip install --disable-pip-version-check -r requirements.txt


# Build image

WORKDIR /usr/src/app
COPY . /usr/src/app
