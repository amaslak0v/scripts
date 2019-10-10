import socket
import socketserver
import json
from ast import literal_eval

""" 
Первое приложение (сервер)
Создать многопоточный TCP-сервер со следующим функционалом: 
– фиксировать все попытки входящих соединений со стороны клиентов
– сервер должен идентифицировать клиента по его ip-адресу и сопоставлять с ним имя (к клиенту в дальнейшем можно обращаться по имени или по ip-адресу)
– организовать постоянный приём и отсылку сообщений от клиентов (каждый клиент должен иметь возможность отправить любому другому присоединенному к серверу клиенту сообщение), сообщения оформляются как команды с помощью JSON, формат команд согласовать с преподавателем
– по требованию клиента сервер должен выдавать список всех присоединенных к нему клиентов (список оформляется с помощью JSON)
"""


class ClientBase:

    def __init__(self):
        self.base = {}
        self.clients = []

    def add_client(self, ip, port):
        cl = self.get_client(ip)
        if cl is None:
            name = 'user_{}'.format(len(self.clients) + 1)
            new_client = Client(name, ip, port)
            self.clients.append(new_client)
            return new_client
        else:
            return cl

    def get_users_json(self):
        for cl in self.clients:
            self.base[cl.name] = cl.ip
        return json.dumps(self.base, indent=4, sort_keys=True)

    def get_client(self, param):
        for cl in self.clients:
            if cl.ip == param:
                return cl
            if cl.name == param:
                return cl
        return None


class Client:

    def __init__(self, name, ip, port):
        self.ip = ip
        self.name = name
        self.port = port

    def __repr__(self):
        return "Name: {}\nIP: {}\nPort: {}".format(self.name, self.ip, self.port)


class MyTCPHandler(socketserver.BaseRequestHandler):

    def __init__(self, request, client_address, server):

        self.clients_base = ClientBase()
        super().__init__(request, client_address, server)

    def handle(self):
        data = self.request.recv(1024).strip()
        data_dict = literal_eval(data.decode())

        ip, port = self.client_address
        client = self.clients_base.add_client(ip, port)
        print("\nConnected -> User: {}, IP: {}".format(client.name, client.ip))
        print('Data received: {}'.format(data_dict))

        response = self.process_request(data_dict)
        if self.clients_base.get_client(data_dict['send_to']):
            self.send_to_other_client(client, response)

        self.request.sendall(response)

    def process_request(self, data):
        if data['command'] == 'get_users':
            response = str(self.get_users_json())
        else:
            response = data['command']
        return bytes(response + "\n", "utf-8")

    def send_to_other_client(self, client, response):
        try:
            print("Sending {} to {}".format(response, client))
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.connect((client.ip, client.port))
                sock.sendall(bytes(response, "utf-8"))
        except ConnectionRefusedError as err:
            print('Connection refused by server. {}'.format(err))

    def get_users_json(self):
        print(self.clients_base.get_users_json())
        return self.clients_base.get_users_json()


if __name__ == '__main__':

    HOST = '0.0.0.0'
    PORT = 80

    with socketserver.TCPServer((HOST, PORT), MyTCPHandler) as server:
        print('Server listening on {}:{}'.format(HOST, PORT))
        # Activate the server; this will keep running until you
        # interrupt the program with Ctrl-C
        server.serve_forever()
