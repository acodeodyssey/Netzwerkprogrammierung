import json
import socket
from threading import Thread


class ClientHandler(Thread):
    def __init__(self, inSocket, address):
        Thread.__init__(self)
        self.socket = inSocket
        self.clientaddress = address
        print("Connection from {}".format(address))

    def run(self):
        while True:
            recievedbytes = inSocket.recv(1024)
            if len(recievedbytes) == 0:
                break
            recievedmsg = recievedbytes.decode("utf-8")
            data = json.loads(recievedmsg)
            if data['type'] == "hello":
                clients.append(data['content'])
                print("Client with Id: " + data['content'][0]['id'] + " said hello")
                self.send("hi client")

    def send(self, msg):
        self.socket.send(str.encode(msg + "\n"))

    def closesock(self):
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
