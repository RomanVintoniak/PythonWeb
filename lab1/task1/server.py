import socket
from time import gmtime, strftime, sleep

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.bind(("127.0.0.1", 5689))
socket.listen()

conn, addr = socket.accept()
serverRunning = True

print(f"\nConnected by {addr}\n")

while serverRunning:
    messageFromClient = conn.recv(1024).decode()
    if (messageFromClient == "exit"):
        serverRunning = False
        conn.close()
    else:
        print(f'[{strftime("%H:%M:%S")}] {messageFromClient}')