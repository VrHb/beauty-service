FROM python:alpine3.17

RUN mkdir -p /home/www

RUN addgroup -S www && adduser -S www -G www

ENV HOME=/home/www
ENV APP_HOME=/home/www/app

RUN mkdir $APP_HOME
RUN mkdir $APP_HOME/staticfiles

WORKDIR $APP_HOME

COPY ./requirements.txt . 

RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

COPY . $APP_HOME

RUN chown -R www:www $APP_HOME

USER www
