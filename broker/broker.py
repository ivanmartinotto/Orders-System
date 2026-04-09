import zmq
import threading
import time

# main broker function
def broker():
    context = zmq.Context()

    # socket that comunicates with the Clients (ROUTER identifies who sent it)
    frontend = context.socket(zmq.ROUTER)
    frontend.bind("tcp://*:5555")

    # socket that comunicates with the Workers
    backend = context.socket(zmq.ROUTER)
    backend.bind("tcp://*:5556")

    # socket that publishes events for the Monitor
    publisher = context.socket(zmq.PUB)
    publisher.bind("tcp://*:5557")

    # Poller: monitor multiple sockets simultaneously (non-blocking)
    poller = zmq.Poller()
    poller.register(frontend, zmq.POLLIN)
    poller.register(backend, zmq.POLLIN)

    # main loop
    while True:
        sockets = dict(poller.poll())

        # Client message arrived -> send to Worker
        if frontend in sockets:
            msg = frontend.recv_multipart()
            publisher.send_string(f"ORDER RECEIVED: {msg[-1].decode()}")
            backend.send_multipart(msg)

        # Worker's response arrived -> send back to the right client
        if backend in sockets:
            msg = backend.recv_multipart()
            publisher.send_string(f"ORDER CONCLUDED: {msg[-1].decode()}")
            frontend.send_multipart(msg)

if __name__ == "__main__":
    broker()
