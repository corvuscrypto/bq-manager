FROM python:alpine3.6
COPY . /code

WORKDIR /code

RUN apk update && apk add \
        gcc \
        musl-dev \
        linux-headers \
        python3-dev \
        make \
        g++ \
        libressl \
        libressl-dev

RUN pip install -r requirements/common.txt

CMD python run.py
