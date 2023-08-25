import socket
import select
import queue

server_address = ('localhost', 10000)

clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

clientsocket.connect(server_address)

while(True):
    print("Enter your message:")
    msg = input()
    msg = msg.encode()

    clientsocket.send(msg)

    msg1 = clientsocket.recv(1024)
    print("The received message is " + msg1.decode())
