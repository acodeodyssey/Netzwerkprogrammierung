import json
import socket
import sys
import time
from threading import Thread

import client

clients = {}


class ClientHandler(Thread):
    def __init__(self, inSocket, address):
        Thread.__init__(self)
        self.socket = inSocket
        self.timeout = time.time() + 30.0
        self.client = client.Client(address, time.time(), 'name')
        self.id = None
        print("Connection from {}".format(address))

    def run(self):
        self.timeout = time.time() + 30.0
        try:
            while self.timeout > time.time():
                recievedbytes = inSocket.recv(1024)
                if len(recievedbytes) == 0:
                    continue
                recievedmsg = recievedbytes.decode("utf-8")
                self.client.lastseen = time.time()
                data = json.loads(recievedmsg)
                msgtype = data['type']

                if msgtype == "hello":
                    self.id = data['id']
                    print("Client with Id:{} said hello ".format(self.id))
                    self.client.info = data['info']
                    clients[self.id] = self.client
                    self.send("hi client")
                    self.timeout += 10.0
                elif msgtype == "beat":
                    print("Client with Id:{} sent heartbeat".format(self.id))
                    self.timeout += 10.0
                else:
                    print("Client sent invalid message")
                    self.timeout += 10.0
            print("Client Timed Out")
        finally:
            del clients[self.id]
            self.closesock()
            sys.exit()


    def send(self, msg):
        self.socket.send(str.encode(msg + "\n"))

    def closesock(self):
        print("Closing Connection")
        self.socket.close()


def showclient(id):
    print("Info for Client with Id: {}".format(id))
    clients[id].printinfo()


def listclients():
    for key, value in clients.items():
        print("showing info for Client with Id: {}".format(key))
        value.printinfo()


if __name__ == "__main__":
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
    host = 'localhost'
    # bind to localhost/port
    s.bind((host, 8443))
    print("Start server at {}:{}".format(host, 8443))
    try:
        while True:
            s.listen(socket.SOMAXCONN)
            inSocket, addr = s.accept()
            clientHandler = ClientHandler(inSocket, addr)
            clientHandler.start()
            listclients()

    finally:
        s.close()
