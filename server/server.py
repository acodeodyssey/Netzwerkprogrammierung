import json
import logging
import os
import socket
import sys
import time
from threading import Thread

import client
import package

clients = {}
packages = {}

class ClientHandler(Thread):
    def __init__(self, inSocket, address):
        """Init Thread with Informaton regarding the Client"""
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
                print(data)

                if msgtype == "hello":
                    self.id = data['id']
                    logging.info("Client with Id:{} said hello ".format(self.id))
                    self.client.info = data['info']
                    clients[self.id] = self.client
                    self.send("hi client")
                    self.timeout += 30.0
                elif msgtype == "beat":
                    print("beat")
                    logging.info("Client with Id:{} sent heartbeat".format(self.id))
                    self.timeout += 30.0
                elif msgtype == "update":
                    pkg = packages.get(data['package'])
                    if pkg is None:
                        self.send(json.dumps({'file': "endTransfer"}))
                        continue
                    self.sendupdate(pkg)
                    time.sleep(1)
                    self.send(json.dumps({'file': "endTransfer"}))
                    self.timeout += 30.0
                elif msgtype == "upgrade":
                    print("upgrade")
                    self.sendupgrade()
                    self.timeout += 30.0
                else:
                    logging.warning("Client sent invalid message")
                    self.timeout += 30.0
            logging.warning("Client Timed Out")
        finally:
            del clients[self.id]
            self.closesock()
            sys.exit()

    def sendupgrade(self):
        """Send Upgrade to client"""
        for key, pkg in packages.items():
            self.sendupdate(pkg)
            time.sleep(1)

        self.send(json.dumps({'file': "endTransfer"}))

    def sendupdate(self, pkg):
        """Send Update of given Package to client"""
        self.send(json.dumps({'name': pkg.name, 'version': pkg.version, 'file': pkg.file}))
        self.sendfile(pkg.file)

    def sendfile(self, file):
        f = open(file, 'rb')
        while True:
            l = f.read(1024)
            if len(l) == 0:
                break
            self.socket.send(l)
            break
        f.close()

    def send(self, msg):
        """"Encode and send msg to client"""
        print(msg)
        self.socket.send(str.encode(msg + "\n"))

    def closesock(self):
        logging.info("Closing Connection")
        self.socket.close()


def indexpackages():
    """Iterates over Packages in Resource Folder and saves the Information in a List"""
    files = os.listdir('resources')
    for file in files:
        details = file.split('.z')
        pkgdetail = details[0].split('_')
        pkg = package.Package(pkgdetail[0], pkgdetail[1], "localhost:8443/resources/{}".format(file),
                              "resources/{}".format(file))
        packages[pkg.name] = pkg

def showclient(id):
    """Prints Information of Client with give Id"""
    print("Info for Client with Id: {}".format(id))
    clients[id].printinfo()


def listclients():
    for key, value in clients.items():
        print("showing info for Client with Id: {}".format(key))
        value.printinfo()


def handleinput():
    """Handle the Server admin input"""
    cmd = input().split()
    if cmd[0] == "show" and len(cmd) == 2:
        showclient(cmd[1])

    elif cmd[0] == "list":
        listclients()

    elif cmd[0] == "help":
        print("List of Commands: \n show -id- \n list \n quit")

    elif cmd[0] == "quit":
        s.close()
        os._exit(1)

    else:
        print("Not a valid Command, for more info read the Readme, or enter the command help")


if __name__ == "__main__":
    indexpackages()
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
