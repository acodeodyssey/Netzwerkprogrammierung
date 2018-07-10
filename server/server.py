import json
import logging
import os
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
                    logging.info("Client with Id:{} said hello ".format(self.id))
                    self.client.info = data['info']
                    clients[self.id] = self.client
                    self.send("hi client")
                    self.timeout += 10.0
                elif msgtype == "beat":
                    logging.info("Client with Id:{} sent heartbeat".format(self.id))
                    self.timeout += 10.0
                else:
                    logging.warning("Client sent invalid message")
                    self.timeout += 10.0
            logging.warning("Client Timed Out")
        finally:
            del clients[self.id]
            self.closesock()
            sys.exit()


    def send(self, msg):
        self.socket.send(str.encode(msg + "\n"))

    def closesock(self):
        logging.info("Closing Connection")
        self.socket.close()


def showclient(id):
    print("Info for Client with Id: {}".format(id))
    clients[id].printinfo()


def listclients():
    for key, value in clients.items():
        print("showing info for Client with Id: {}".format(key))
        value.printinfo()


def handleinput():
    cmd = input().split()
    if cmd[0] == "show" and len(cmd) == 2:
        showclient(cmd[1])

    elif cmd[0] == "list":
        listclients()

    elif cmd[0] == "quit":
        s.close()
        os._exit(1)

    else:
        print("Not a valid Command, for more info, read the Readme")


if __name__ == "__main__":
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
    host = 'localhost'
    # bind to localhost/port
    s.bind((host, 8443))
    print("Start server at {}:{}".format(host, 8443))
    try:
        while True:
            i = Thread(target=handleinput, args=[])
            i.start()
            s.listen(socket.SOMAXCONN)
            inSocket, addr = s.accept()
            clientHandler = ClientHandler(inSocket, addr)
            clientHandler.start()

    finally:
        s.close()
