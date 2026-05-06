FROM python:3.11-slim

WORKDIR /app

COPY worker/requirements.txt .
RUN pip install -r requirements.txt

RUN playwright install chromium
RUN playwright install-deps chromium

COPY worker/ .

CMD ["python", "worker.py"]