FROM alpine:3.7 as builder


RUN mkdir -p /code \
 && apk add --no-cache --update python3 py3-pip su-exec \ 
 && pip3 install --upgrade pip \
 && pip3 install virtualenv \
 && virtualenv /code/venv 

WORKDIR /code/anakin
COPY ./anakin .
RUN . /code/venv/bin/activate \
 && python3 setup.py install

WORKDIR /code/dbio
COPY ./dbio .
RUN . /code/venv/bin/activate \
 && python3 setup.py install

WORKDIR /code/never
COPY ./never .
RUN . /code/venv/bin/activate \
 && python3 setup.py install


COPY ./entry.sh /code
WORKDIR /code/storage
RUN adduser \
    -DS \
    -s /bin/nologin \
    -h /code/storage \
    never

RUN mkdir -p /code/storage/stash \
 && chown never:nogroup /code/storage/stash 

ENTRYPOINT ["/sbin/su-exec", "never", "/code/entry.sh"]
#ENTRYPOINT ["/sbin/su-exec", "never", "ash"]

