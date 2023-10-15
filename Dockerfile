FROM python:3.11.2
LABEL maintainer="Digital future"

RUN pip install poetry==1.3.2
ENV HOME_DIR = /usr/photoapp
WORKDIR $HOME_DIR
ENTRYPOINT [ "poetry", "run", "python", "./main.py"]

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY .env .
COPY . .
RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi --without dev,test
