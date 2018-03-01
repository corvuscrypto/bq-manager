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

# install gcloud sdk
RUN curl https://dl.google.com/dl/cloudsdk/release/google-cloud-sdk.tar.gz > /tmp/google-cloud-sdk.tar.gz
RUN mkdir -p /usr/local/gcloud
RUN tar -C /usr/local/gcloud -xvf /tmp/google-cloud-sdk.tar.gz
RUN /usr/local/gcloud/google-cloud-sdk/install.sh
ENV PATH $PATH:/usr/local/gcloud/google-cloud-sdk/bin

RUN pip install -r requirements/common.txt

CMD gunicorn --reload -c gunicorn.conf.py run:app
