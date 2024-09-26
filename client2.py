import socket
import threading
import time

# Server details
PORT = 5050
HOST = socket.gethostbyname(socket.gethostname())
ADDR = (HOST, PORT)
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"

# Client-side connect function
def client_connect():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)
    print(f"Connected to the server on {HOST}:{PORT}")
    return client

# Handle receiving messages from the server
def receive_messages(client):
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if message:
                print(message)
        except:
            print("An error occurred.")
            client.close()
            break

# Client-side send function
def send_messages(client):
    while True:
        msg = input("Message (q for quit): ")
        if msg == 'q':
            break
        client.send(msg.encode(FORMAT)) 
        print("Sent message to server successfully...")

    client.send(DISCONNECT_MESSAGE.encode(FORMAT))
    time.sleep(1)
    print('Disconnected')
    client.close()

# Connect to the server and start the client
def start():
    client = client_connect()

    # Start two threads: one for receiving and one for sending messages
    receive_thread = threading.Thread(target=receive_messages, args=(client,))
    receive_thread.start()

    send_thread = threading.Thread(target=send_messages, args=(client,))
    send_thread.start()

if __name__ == "__main__":
    start()
