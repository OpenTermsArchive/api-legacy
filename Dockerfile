FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8-slim

# INSTALL REQUIREMENTS
COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt
RUN apt-get update -y
RUN apt-get install curl unzip cron -y

# SETUP CRON
COPY ./crontab /etc/cron.d/check-for-data
RUN chmod 0644 /etc/cron.d/check-for-data

# DOWNLOAD DATASET
COPY ./download_dataset.sh /download_dataset.sh
RUN chmod +x /download_dataset.sh
RUN source /download_dataset.sh

# COPY AND RUN APP
COPY ./app /app

CMD service cron start && /start.sh