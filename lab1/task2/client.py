import socket
import threading

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
nickname = input("Enter your nickname: ")

address = "127.0.0.1"
port = 55555

client.connect((address, port))


def recive():
    while True:
        try:
            message = client.recv(1024).decode()
            if message == "NICK":
                client.send(nickname.encode())
            else:
                print(message)
        except:
            print("An error occurred !")        
            client.close()
            break
                

def write():
    while True:
        message = f'{nickname}: {input("")}'
        client.send(message.encode())


receiveThreed = threading.Thread(target=recive)
receiveThreed.start()

writeThread = threading.Thread(target=write)
writeThread.start()