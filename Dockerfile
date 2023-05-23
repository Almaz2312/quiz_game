FROM python:3.10-slim-bullseye
ENV PYTHONBUFFERED=1

WORKDIR /quiz_game

COPY . .

RUN pip install --upgrade pip \
&& pip install poetry \
&& poetry config virtualenvs.create false \
&& poetry install --no-root
