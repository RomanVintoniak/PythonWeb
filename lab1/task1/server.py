import socket
from time import gmtime, strftime, sleep

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.bind(("127.0.0.1", 5689))
socket.listen()

conn, addr = socket.accept()
print(f"\nConnected by {addr}\n")

messageFromClient = conn.recv(1024)
sleep(5)

if len(messageFromClient) == 44:
    respons = 'All data received successfully'
else:
    respons = 'Data transmission error'

conn.send(respons.encode())
conn.close()