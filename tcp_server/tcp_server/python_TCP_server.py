#!/usr/local/bin/python
import socket
import threading

bind_ip = '0.0.0.0'
bind_port = 8081

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((bind_ip, bind_port))
server.listen(5)  # max backlog of connections

print('Listening on {}:{}'.format(bind_ip, bind_port))
active_connections = []


def handle_client_connection(client_socket):
    request = client_socket.recv(1024)
    print('Received {}'.format(request))
    client_socket.send("Maslakou's TCP-server")
    client_socket.close()

def duplicate_client_check(addr):

    if addr in active_connections:
        print("Duplicate client!")
        client_sock.close()
        return False
    else:
        active_connections.append(addr)
        print(active_connections)
        return True


while True:
    client_sock, address = server.accept()
    #print address[0]
      
    if duplicate_client_check(address[0]):
        print('Accepted connection from {}:{}'.format(address[0], address[1]))
        client_handler = threading.Thread(
            target=handle_client_connection,
            args=(client_sock,) 
        )
        client_handler.start()
    else:
        print("Connection refused!")
