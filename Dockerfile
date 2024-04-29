FROM python:slim

WORKDIR /work

COPY requirements.txt .

RUN pip install --no-cache-dir -U -r requirements.txt

COPY . .
