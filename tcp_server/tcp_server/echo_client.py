import socket

"""
Второе приложение (клиент)
Организовать отсылку команд серверу (сообщений и управляющих команд). Команды с параметрами вводятся пользователем с клавиатуры.
"""

HOST = '0.0.0.0'  # The server's hostname or IP address
PORT = 8080       # The port used by the server

print("input 'get_users' to get list of all users")
command = str(input('Input command:'))
data = "{'send_to': 'user_1', 'command': '"+command+"'}"

# Create a socket (SOCK_STREAM means a TCP socket)
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    # Connect to server and send data
    sock.connect((HOST, PORT))
    sock.sendall(bytes(data, "utf-8"))

    # Receive data from the server and shut down
    received = str(sock.recv(1024), "utf-8")

print("Sent:     {}".format(data))
print("Received: {}".format(received))