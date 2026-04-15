import zmq
import time 
import os
from datetime import datetime

BROKER_HOST = os.getenv("BROKER_HOST", "localhost")

counters = {"Received": 0, "Concluded": 0}

def monitor():
    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    socket.connect(f"tcp://{BROKER_HOST}:5557")
    socket.setsockopt_string(zmq.SUBSCRIBE, "") # subscribe to all topics

    print("[MONITOR] Observing the system in real time. \n", flush=True)
    print(f"{'HOUR':<12} {'EVENT':<20} {'DETAIL'}")
    print("-"*50)

    while True:
        event = socket.recv_string()
        hour = datetime.now().strftime("%H:%M:%S")

        if event.startswith("ORDER RECEIVED"):
            counters["Received"] += 1
            detail = event.split(":", 1)[1]
            print(f"{hour:<12} {'RECEIVED':<20} {detail}", flush=True)

        elif event.startswith("ORDER CONCLUDED"):
            counters["Concluded"] += 1
            detail = event.split(":", 1)[1]
            print(f"{hour:<12} {'CONCLUDED':<20} {detail}", flush=True)
            print(f" Recebidos: {counters['Received']} | Concluídos: {counters['Concluded']}", flush=True)


if __name__ == "__main__":
    time.sleep(2)
    monitor()