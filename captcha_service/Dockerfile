FROM python:3.10-slim

# Install system dependencies
RUN apt-get update && \
    apt-get install -y libpq-dev gcc

WORKDIR /captcha_service
COPY . /captcha_service

RUN pip install --no-cache-dir -r requirements.txt
CMD python ./main.py
