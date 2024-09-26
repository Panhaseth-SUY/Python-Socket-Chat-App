import socket
import threading

# Server details
PORT = 5050
HOST = socket.gethostbyname(socket.gethostname())
ADDR = (HOST, PORT)
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"

# Global variables
clients = []
clients_lock = threading.Lock()

def server_bind():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen()
    print(f"Server listening on {HOST}:{PORT}")
    return server

# Broadcast message to all clients
def broadcast(message, conn):
    with clients_lock:
        for client in clients:
            if client != conn:
                try:
                    client.send(message)
                except:
                    clients.remove(client)


# Handle individual client connection
def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} Connected")
    connected = True
    while connected:
        try:
            message = conn.recv(1024)
            if message == DISCONNECT_MESSAGE:
                connected = False
            elif message:
                print(f"Client-[{addr}] {message.decode('utf-8')}")
                broadcast(message, conn)
        except:
            connected = False

    with clients_lock:
        clients.remove(conn)
    conn.close()

# Start the server and listen for connections
def start():
    server = server_bind()
    print('[SERVER STARTED]!')
    while True:
        conn, addr = server.accept()
        with clients_lock:
            clients.append(conn)
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")

if __name__ == "__main__":
    start()
