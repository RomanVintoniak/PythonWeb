import socket

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.connect(("127.0.0.1", 5689))

print("Send something to the server\n")
print("> ", end="")

messageToServer = input()
socket.send(messageToServer.encode())