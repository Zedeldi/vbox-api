# syntax=docker/dockerfile:1

FROM python:3

WORKDIR /usr/src/app

COPY . .
RUN pip install --no-cache-dir .

CMD ["vbox-api-http"]
