import uuid
import socket
import sys
import os


class MyClient:
    def __init__(self, s=None):
        # initialize socket
        if s is None:
            self.s = socket.socket(socket.AF_INET,
                                   socket.SOCK_STREAM, socket.IPPROTO_TCP)
        else:
            self.s = s
        # initialize info and id
        self.host = sys.argv[1]
        self.port = int(sys.argv[2])
        osinfo = os.uname()
        id = uuid.uuid1()
        self.info = [id, osinfo]

    def connect(self, host, port):
        self.s.connect((host, port))
        self.local = self.s.getsockname()
        self.remote = self.s.getpeername()

    def send(self):
        if len(sys.argv) >= 4:
            cmd = sys.argv[3]
        # send cmd
        if cmd is not None:
            # convert cmd into byte array
            self.sentbytes = self.s.send(bytes(cmd+"\n", 'utf-8'))

    def receive(self):
        while True:
            recievedbytes = self.s.recv(10)
            if (len(recievedbytes) == 0):
                break
            print(recievedbytes.decode('utf-8'))

    def disconnect(self):
        self.s.close()
