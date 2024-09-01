FROM python:3.10-slim

# Install system dependencies
RUN apt-get update && \
    apt-get install -y libpq-dev gcc


WORKDIR /api_gateway
COPY . /api_gateway

RUN pip install --no-cache-dir -r requirements.txt


EXPOSE 8000

CMD ["sh", "-c", "python api_gateway/manage.py makemigrations && \
                   python api_gateway/manage.py migrate && \
                   python api_gateway/manage.py runserver 0.0.0.0:8000"]
