FROM python:3.8-alpine

RUN apk update && apk add build-base
RUN apk add --no-cache -X http://dl-cdn.alpinelinux.org/alpine/edge/testing hdf5-dev

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

COPY . /app

ENV ESDG_DATABASE_PATH=/db/database.hdf5

CMD ["uvicorn", "main:app", "--host", "0.0.0.0"]