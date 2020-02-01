FROM python:3.8-alpine

RUN apk update && apk add build-base
RUN apk add --no-cache -X http://dl-cdn.alpinelinux.org/alpine/edge/testing hdf5-dev

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

EXPOSE 80

COPY . /app

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]