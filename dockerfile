FROM python:3.12-slim

WORKDIR /app

COPY dev-req.txt .
RUN pip install --no-cache-dir -r dev-req.txt

COPY . .

