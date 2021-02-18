FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8-slim

COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt
RUN apt-get update -y
RUN apt-get install curl unzip -y
COPY ./download_dataset.sh /download_dataset.sh
RUN chmod +x /download_dataset.sh
RUN /download_dataset.sh

COPY ./app /app
