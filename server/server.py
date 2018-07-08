import json
import socket
import sys
import time
from threading import Thread


class ClientHandler(Thread):
    def __init__(self, inSocket, address):
        Thread.__init__(self)
        self.timeout = time.time() + 60
        self.socket = inSocket
        self.clientaddress = address
        self.id = None
        print("Connection from {}".format(address))

    def run(self):
        try:
            while self.timeout > time.time():
                recievedbytes = inSocket.recv(1024)
                if len(recievedbytes) == 0:
                    break
                recievedmsg = recievedbytes.decode("utf-8")
                data = json.loads(recievedmsg)
                msgtype = data['type']
                if msgtype == "hello":
                    self.id = data['content'][0]['id']
                    clients.append(data['content'])
                    print("Client with Id:{} said hello ".format(self.id))
                    self.send("hi client")
                elif msgtype == "beat":
                    print("Client with Id:{} send heartbeat".format(self.id))
                    self.timeout += 30
                else:
                    print("Client sent invalid message")
                    self.timeout += 30
        finally:
            print("Client Timed Out")
            self.closesock()
            sys.exit()

    def send(self, msg):
        self.socket.send(str.encode(msg + "\n"))

    def closesock(self):
        print("Closing Connection")
        self.socket.close()


if __name__ == "__main__":
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
    host = 'localhost'
    clients = []
    # bind to localhost/port
    s.bind((host, 8443))
    print("Start server at {}:{}".format(host, 8443))
    try:
        while True:
            s.listen(socket.SOMAXCONN)
            inSocket, addr = s.accept()
            clientHandler = ClientHandler(inSocket, addr)
            clientHandler.start()

    finally:
        s.close()
