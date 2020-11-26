FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8-slim

RUN apt-get update -y
RUN apt-get install curl -y
RUN curl -LJS https://github.com/ambanum/CGUs-versions/releases/download/2020-11-23-16e3f34/dataset-2020-11-23-16e3f34.zip -o dataset.zip

RUN apt-get install unzip -y
RUN unzip dataset.zip && mv dataset-2020-11-23-16e3f34 dataset

COPY ./app /app
