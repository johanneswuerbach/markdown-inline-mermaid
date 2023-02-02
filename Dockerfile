FROM python:3-alpine

RUN apk add --no-cache nodejs npm chromium

RUN npm install -g @mermaid-js/mermaid-cli

WORKDIR /app

COPY requirements_test.txt .

RUN pip install -r requirements_test.txt

COPY . .

RUN pip install .
