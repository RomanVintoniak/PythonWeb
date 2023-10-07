import socket
from time import gmtime, strftime

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.bind(("127.0.0.1", 5689))
socket.listen()

conn, addr = socket.accept()

print(f"Message from client:\n")

messageFromClient = conn.recv(1024).decode()
print(f"{strftime('%H:%M:%S')}  {messageFromClient}")