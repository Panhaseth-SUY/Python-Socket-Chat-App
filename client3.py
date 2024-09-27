import socket
import threading
import time
import datetime
import tkinter as tk
from tkinter import scrolledtext, messagebox

# Server details
PORT = 5050
HOST = socket.gethostbyname(socket.gethostname())
ADDR = (HOST, PORT)
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"

# Global client variable
client = None

# GUI Class
class ChatClientGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Chat Client")
        self.root.geometry("500x600")
        
        # Username Label and Entry
        self.username_label = tk.Label(root, text="Username:")
        self.username_label.pack(pady=5)
        self.username_label.config(font=("Arial", 16,"bold"))
        self.username_entry = tk.Entry(root, width=50)
        self.username_entry.pack(pady=5)
        self.username_entry.focus()

        # Connect Button
        self.connect_button = tk.Button(root, text="Connect", command=self.connect_to_server, width=10, border=3)
        self.connect_button.pack(pady=5)
        self.connect_button.config(font=("Arial", 16,"bold"))

        # Message display (ScrolledText)
        self.chat_display = scrolledtext.ScrolledText(root, width=60, height=20, state='disabled')
        self.chat_display.pack(pady=10)

        # Message Entry and Send Button
        self.message_entry = tk.Entry(root, width=50, border=3)
        self.message_entry.pack(pady=5)
        self.message_entry.focus()
        self.message_entry.config(font=("Arial", 16))

        self.send_button = tk.Button(root, text="Send", command=self.send_message, state='disabled', width=10, border=3)
        self.send_button.pack(pady=5)
        self.send_button.config(font=("Arial", 16,"bold"))


        # Disconnect Button
        self.disconnect_button = tk.Button(root, text="Disconnect", command=self.disconnect, state='disabled', width=10, border=3)
        self.disconnect_button.pack(pady=5)
        self.disconnect_button.config(font=("Arial", 16,"bold"))

    # Connect to the server
    def connect_to_server(self):
        global client
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            username = self.username_entry.get()
            if not username:
                messagebox.showerror("Error", "Username cannot be empty!")
                return

            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect(ADDR)
            formatted_message = f"{current_time}\n{username}: Enter the room...\n"
            client.send(formatted_message.encode(FORMAT))

            self.chat_display.config(state='normal')
            self.chat_display.insert(tk.END, f"Connected to the server on {HOST}:{PORT}\n")
            self.chat_display.config(state='disabled')

            self.connect_button.config(state='disabled')
            self.send_button.config(state='normal')
            self.disconnect_button.config(state='normal')

            # Start a thread to receive messages
            receive_thread = threading.Thread(target=self.receive_messages)
            receive_thread.start()

        except Exception as e:
            messagebox.showerror("Connection Error", str(e))

    # Receive messages from the server
    def receive_messages(self):
        while True:
            try:
                message = client.recv(1024).decode(FORMAT)
                if message:
                    self.chat_display.config(state='normal')
                    self.chat_display.insert(tk.END, f"\n{message}")
                    self.chat_display.config(state='disabled')
            except:
                self.chat_display.config(state='normal')
                self.chat_display.insert(tk.END, "\nAn error occurred. Disconnecting...\n")
                self.chat_display.config(state='disabled')
                client.close()
                break

    # Send messages to the server
    def send_message(self):
        try:
            message = self.message_entry.get()
            if not message:
                return

            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            username = self.username_entry.get()
            formatted_message = f"{current_time}\n{username}: {message}\n"
            client.send(formatted_message.encode(FORMAT))

            self.chat_display.config(state='normal')
            self.chat_display.insert(tk.END, f"{current_time}\nYou: {message}")
            self.chat_display.config(state='disabled')

            self.message_entry.delete(0, tk.END)

        except Exception as e:
            messagebox.showerror("Error", f"Failed to send message: {e}")

    # Disconnect from the server
    def disconnect(self):
        try:
            client.send(DISCONNECT_MESSAGE.encode(FORMAT))
            client.close()

            self.chat_display.config(state='normal')
            self.chat_display.insert(tk.END, "\nDisconnected from server.\n")
            self.chat_display.config(state='disabled')

            self.send_button.config(state='disabled')
            self.disconnect_button.config(state='disabled')
            self.connect_button.config(state='normal')

        except Exception as e:
            messagebox.showerror("Error", str(e))

# Main function
def main():
    root = tk.Tk()
    gui = ChatClientGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
