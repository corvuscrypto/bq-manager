FROM python:alpine3.6

RUN apk update && apk add \
        gcc \
        musl-dev \
        linux-headers \
        python3-dev \
        make \
        g++ \
        libressl \
        libressl-dev

RUN pip install google-cloud==0.32.0 \
                pymongo==3.6.0 \
                structlog==17.2.0
