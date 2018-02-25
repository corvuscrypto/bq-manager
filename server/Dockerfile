FROM alpine:python-3.6
COPY . /code

CMD gunicorn --reload -c gunicorn.conf.py run:app
