FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY simulator ./simulator

ENV PYTHONPATH=/app
CMD ["python", "-m", "simulator.main"]
