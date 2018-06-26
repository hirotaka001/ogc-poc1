FROM python:3.6.5-alpine
MAINTAINER Nobuyuki Matsui <nobuyuki.matsui@gmail.com>

ARG LISTEN_PORT
ENV LISTEN_PORT ${LISTEN_PORT:-3000}

COPY ./app /opt/storage

WORKDIR /opt/storage

RUN apk update && \
    apk add --no-cache nginx supervisor && \
    apk add --no-cache --virtual .build python3-dev build-base linux-headers pcre-dev && \
    apk add --no-cache --virtual .pillow jpeg-dev zlib-dev freetype-dev lcms2-dev openjpeg-dev \
                                         tiff-dev tk-dev tcl-dev harfbuzz-dev fribidi-dev && \
    pip install -r requirements/common.txt && \
    pip install -r requirements/production.txt && \
    rm /etc/nginx/nginx.conf && \
    apk del --purge .build && \
    rm -r /root/.cache

COPY nginx.conf /etc/nginx/nginx.conf
COPY flask-nginx.conf /etc/nginx/conf.d/flask-nginx.conf
COPY uwsgi.ini /etc/uwsgi/uwsgi.ini
COPY supervisord.conf /etc/supervisord.conf
COPY entrypoint.sh /opt

RUN chmod a+x /opt/entrypoint.sh

ENTRYPOINT /opt/entrypoint.sh
