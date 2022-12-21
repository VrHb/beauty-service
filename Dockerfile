FROM python:alpine3.17

RUN mkdir -p /app

WORKDIR /app

COPY . . 

RUN apk add --no-cache vim htop

RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

RUN python3 manage.py collectstatic
