FROM  python:3.10.12-alpine

WORKDIR  /App

COPY sqlite.db.init sqlite.db

COPY  requirements.txt ./
RUN  pip install -r requirements.txt

COPY  . .
ENV  FLASK_APP = app.py
ENV  FLASK_ENV = production
ENV  FLASK_DEBUG = 0
EXPOSE  5000

CMD  gunicorn --bind 0.0.0.0:5000 -w 1 app:app


