# Quickstart

## Prerequisites

- Docker + Docker Compose
- Python 3.10+
- Node 18+
- Optional: `kubectl` + kind/minikube

## Docker Compose

```bash
cp .env.example .env

docker-compose up --build
```

UI: http://localhost:5173

## Kafka CLI examples

```bash
# list topics
kafka-topics.sh --bootstrap-server localhost:9092 --list

# create topics
kafka-topics.sh --bootstrap-server localhost:9092 --create --topic hf.signals --partitions 3 --replication-factor 1
kafka-topics.sh --bootstrap-server localhost:9092 --create --topic hf.alerts --partitions 1 --replication-factor 1

# consumer groups
kafka-consumer-groups.sh --bootstrap-server localhost:9092 --list
```

## Local dev

See `README.md` for bare-metal commands.
