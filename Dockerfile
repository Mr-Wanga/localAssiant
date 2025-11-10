FROM python:3.14-slim

COPY . .
RUN pip install -r requirements.txt
