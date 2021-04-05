FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8-slim
ARG COMMIT=""
LABEL commit=${COMMIT}
ENV COMMIT_SHA=${COMMIT}

# INSTALL REQUIREMENTS
COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt
RUN apt-get update -y --fix-missing
RUN apt-get install nano curl unzip cron rsyslog -y

# SETUP CRON
COPY ./crontab /etc/cron.d/check-for-data
RUN chmod 0644 /etc/cron.d/check-for-data
COPY ./check_for_data.sh /check_for_data.sh
RUN chmod +x /check_for_data.sh
RUN crontab /etc/cron.d/check-for-data

# DOWNLOAD DATASET
COPY ./download_dataset.sh /download_dataset.sh
RUN chmod +x /download_dataset.sh
RUN /download_dataset.sh

# COPY AND RUN APP
COPY ./app /app

CMD service cron start && /start.sh
