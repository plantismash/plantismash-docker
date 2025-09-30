FROM python:2.7

RUN git clone https://github.com/plantismash/webserver.git -b dev webserver; \
    cd webserver; \
    pip install -r requirements.txt; \
    pip install uwsgi

RUN groupadd -g 1004 plantismash
RUN useradd plantismash -u 1002 -g 1004

USER 1002:1004

COPY ./settings.cfg /webserver/settings.cfg

ENV WEBSMASH_CONFIG=/webserver/settings.cfg

WORKDIR /webserver

STOPSIGNAL SIGINT

CMD uwsgi --workers 12 --pythonpath /var/www --http :8950 --module websmash:app --touch-reload /tmp/reload_websmash

EXPOSE 8950
