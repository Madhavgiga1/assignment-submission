FROM python:3.9-alpine3.13
LABEL maintainer="madhav.com"
ENV PYTHONUNBUFFERED 1

WORKDIR /app 

COPY ./app /app
COPY ./requirements.txt /tmp/requirements.txt

EXPOSE 8000


RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    apk add --update --no-cache postgresql-client && \
    apk add --update --no-cache --virtual .tmp-build-deps \
        build-base postgresql-dev musl-dev  && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    apk del .tmp-build-deps && \
    rm -rf /tmp && \
    adduser \
        --disabled-password \
        --no-create-home \
        django-user 


ENV PATH="/py/bin:$PATH"  

USER django-user

