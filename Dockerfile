FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8-slim

COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt
RUN apt-get update -y
RUN apt-get install curl -y
RUN curl -LJS https://github.com/ambanum/CGUs-versions/releases/download/2021-02-15-18df44e/dataset-2021-02-15-18df44e.zip -o dataset.zip

RUN apt-get install unzip -y
RUN unzip dataset.zip && mv dataset-2021-02-15-18df44e dataset

COPY ./app /app
