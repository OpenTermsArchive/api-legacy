FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8-slim

COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt
RUN apt-get update -y
RUN apt-get install curl -y
RUN curl -LJS https://github.com/ambanum/CGUs-versions/releases/download/2021-01-06-e365c67/dataset-2021-01-06-e365c67.zip -o dataset.zip

RUN apt-get install unzip -y
RUN unzip dataset.zip && mv dataset-2020-11-23-16e3f34 dataset

COPY ./app /app
