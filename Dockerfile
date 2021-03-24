FROM python:3.9

ADD backend /backend

WORKDIR /backend

ENV PYTHONPATH /backend
