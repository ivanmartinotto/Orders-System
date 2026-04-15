# Orders System

A simple order processing system implemented with ZeroMQ and Docker Compose.

## Overview

This project demonstrates a lightweight distributed architecture for sending orders from clients to a broker, processing them with a worker, and emitting live events to a monitor.

- `broker/` runs a ZeroMQ ROUTER/DEALER broker and publishes order events.
- `client/` runs a ZeroMQ DEALER client that sends sample orders.
- `worker/` runs a ZeroMQ DEALER worker that processes orders asynchronously.
- `monitor/` runs a ZeroMQ SUB subscriber that listens for broker events.

## Architecture

1. Clients connect to the broker on `tcp://broker:5555` and send order messages.
2. The broker routes incoming orders to workers over `tcp://*:5556`.
3. The worker processes each order in a separate thread and returns the result to the broker.
4. The broker sends completion responses back to the original client.
5. The broker also publishes `ORDER RECEIVED` and `ORDER CONCLUDED` events on `tcp://*:5557` for monitoring.

## Requisites

- Docker
- Docker Compose
- A machine with network access between Docker containers

## Run the system

From the project root directory:

```bash
docker compose up --build
```

This command builds the four service images and starts:

- `broker`
- `client-1`
- `client-2`
- `worker`
- `monitor`

## What to expect

- Each client sends 5 orders.
- The broker forwards orders to the worker and publishes event notifications.
- The worker simulates order processing delays and returns `READY:<order>:by:<worker-id>`.
- The monitor prints live `RECEIVED` and `CONCLUDED` events with counters.

## Notes

- The project uses `pyzmq` inside each container.
- Environment variables like `BROKER_HOST` and `CLIENT_ID` are set in `docker-compose.yml`.
- The worker uses threads so it can process multiple orders without blocking the receive loop.
