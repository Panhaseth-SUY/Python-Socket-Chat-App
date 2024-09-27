from client3 import ChatClientGUI
import tkinter as tk
from tkinter import scrolledtext, messagebox

# Main function
def main():
    root = tk.Tk()
    gui = ChatClientGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()

