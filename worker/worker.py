import zmq
import time
import random
import os
import threading

BROKER_HOST = os.getenv("BROKER_HOST", "localhost")
WORKER_ID   = os.getenv("WORKER_ID", "worker-1")

def process_order(order: str) -> str:
    # emulates the praparation time of the order
    delay = random.uniform(10, 30)
    print(f"[{WORKER_ID}] Processing '{order}' (it's going to take {delay:.1f}s)...", flush=True)
    time.sleep(delay)
    return f"READY:{order}:by:{WORKER_ID}"

def worker():
    context = zmq.Context()
    socket = context.socket(zmq.DEALER)
    socket.connect(f"tcp://{BROKER_HOST}:5556")

    while True:
        # receives: [client_id, empty_frame, message]
        msg = socket.recv_multipart()
        identity = msg[0]
        order     = msg[-1].decode()

        # Processa em thread separada para não bloquear novos pedidos
        def handle(ident, ped):
            response = process_order(order)
            socket.send_multipart([ident, b"", response.encode()])

        t = threading.Thread(target=handle, args=(identity, order))
        t.daemon = True
        t.start()

if __name__ == "__main__":
    time.sleep(2)
    worker()