FROM python:3.8

ENV PYTHONUNBUFFERED 1

COPY . .

RUN pip install --upgrade pip
RUN pip install pipenv

RUN PIPENV_VENV_IN_PROJECT=1 pipenv install --system --deploy
