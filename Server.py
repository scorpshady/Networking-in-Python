import socket
import select
import queue


bindingAddress = ('127.0.0.1', 10000)
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind(bindingAddress)

server.setblocking(0)
server.listen(5)

inputs = [server]
outputs = []
connections = dict()


while(True):
    readable, writable, exception  = select.select(inputs, outputs, [])

    for s in readable:
        if s is server:
            connection, port = s.accept()
            connection.setblocking(0)
            connections[connection] = queue.Queue()             # to later fetch data from it
            inputs.append(connection)
        else:
            data = s.recv(1024)
            if data:
                connections[s].put(data)
                print("In Readable " , s.getpeername())
                
                if s not in outputs:
                    outputs.append(s)
            else:
                #connection is closed
                if s in outputs:
                    outputs.remove(s)
                inputs.remove(s)
                s.close()
                del connections[s]
    
    for s in writable:
        try:
            msg = connections[s].get_nowait()
        except queue.Empty:
            outputs.remove(s)
        else:
            msg1 = "Received message from {socket}".format(socket = s.getpeername())
            msg1 = msg1.encode()
            s.send(msg1)
    
    for s in exception:
        inputs.remove(s)
        if s in outputs:
            outputs.remove(s)
        del connections[s]
