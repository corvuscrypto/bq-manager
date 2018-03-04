FROM corvuscrypto/bq-manager-base:latest
COPY . /code

WORKDIR /code

RUN pip install -r requirements/common.txt

CMD exec gunicorn --reload -c gunicorn.conf.py run:app
