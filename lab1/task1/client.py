import socket

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.connect(("127.0.0.1", 5689))
clientRuning = True

print("\nSend something to the server")

while clientRuning:
    print("> ", end="")
    messageToServer = input()
    socket.send(messageToServer.encode())
    
    if (messageToServer == "exit"):
        clientRuning = False
        socket.close()