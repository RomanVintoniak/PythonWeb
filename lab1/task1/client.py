import socket

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.connect(("127.0.0.1", 5689))

messageToServer = "This is a test message with 44 bytes of data"
print(f"\n> {messageToServer}")

socket.send(messageToServer.encode())

messageFromServer = socket.recv(1024).decode()
print(f"\nReceived from server: {messageFromServer}\n")