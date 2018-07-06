import json
import socket
import time
from threading import Thread


class MyServer():
    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
        self.host = 'localhost'
        self.clients = []
        # bind to localhost/port
        self.s.bind((self.host, 8443))
        self.s.listen(socket.SOMAXCONN)
        print("Start server at {}:{}".format(self.host, 80))

    def acceptclients(self):
        try:
            while True:
                inSocket, addr = self.s.accept()
                print("Connection from {}".format(addr))

        finally:
            self.s.close()

        def handleclient(self):
            while True:
                recievedbytes = inSocket.recv(1024)
                if len(recievedbytes) == 0:
                    break
                recievedmsg = recievedbytes.decode("utf-8")
                data = json.loads(recievedmsg)
                if data['type'] == "hello":
                    self.clients.append(data['content'])
                    print("Client with Id: " + data['content'][0]['id'] + " said hello")
            inSocket.send(str.encode("hello\n "))
            inSocket.close()

if __name__ == "__main__":
    server = MyServer()
    server.acceptclients()
