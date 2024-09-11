FROM python:3.10-slim

# Install system dependencies
RUN apt-get update && \
    apt-get install -y libpq-dev gcc

WORKDIR /comments_service
COPY . /comments_service

RUN pip install --no-cache-dir -r requirements.txt
CMD python ./main.py
