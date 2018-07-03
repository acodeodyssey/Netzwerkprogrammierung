import platform
import socket
import uuid


class MyClient:
    def __init__(self, s=None):
        # initialize socket
        if s is None:
            self.s = socket.socket(socket.AF_INET,
                                   socket.SOCK_STREAM,
                                   socket.IPPROTO_TCP)
        else:
            self.s = s
        self.id = str(uuid.uuid1())
        self.info = {'machine': platform.machine(),
                     'architecture': platform.architecture()}

    def connect(self, host, port):
        self.s.connect((host, port))
        self.local = self.s.getsockname()
        self.remote = self.s.getpeername()

    def send(self, msg):
        serialized = str.encode(msg+"\n")
        print("Sending Message: " + msg)
        self.s.send(serialized)
        self.s.close()
