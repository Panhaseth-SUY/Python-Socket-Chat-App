import socket
import threading
from client import *

# Connect to the server and start listening for messages
def start():
    try:
        client = client_connect()
    except socket.error as e:
        print(f"Error: {e}")
        return
    # Start a thread to receive messages
    receive_thread = threading.Thread(target=receive_messages, args=(client,))
    receive_thread.start()


if __name__ == "__main__":
    start()
