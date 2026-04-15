import zmq
import time
import random 
import os

BROKER_HOST = os.getenv("BROKER_HOST", "localhost")
CLIENT_ID = os.getenv("CLIENT_ID", "client-1")

ORDERS = ["pizza", "cheeseburger", "sushi", "tacos", "ice cream"]

# main client function
def client():
    context = zmq.Context()
    socket = context.socket(zmq.DEALER)

    # unique identity for the broker to know who to respond
    socket.identity = CLIENT_ID.encode()
    socket.connect(f"tcp://{BROKER_HOST}:5555")

    for i in range(5): # send 5 orders
        order = f"{i+1} --- {random.choice(ORDERS)}"
        print(f"[{CLIENT_ID}] Sending order: {order}")
        socket.send_string(order)

        # wait for response
        response = socket.recv_string()
        print(f"[{CLIENT_ID}] Response received: {response}")

        time.sleep(random.uniform(0.5, 2))

    print(f"[CLIENT_ID] All orders concluded.")

if __name__ == "__main__":
    time.sleep(2) # wait broker go up
    client()