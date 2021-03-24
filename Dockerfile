FROM python:3.9

ADD backend /backend

WORKDIR /backend
RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-dev

ENV PYTHONPATH /backend
