import logging
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
        self.info = [{'release': platform.release(),
                      'architecture': platform.architecture()}]
        self.local = None
        self.remote = None

    def connect(self, host, port):
        try:
            self.s.connect((host, port))
        except socket.error:
            logging.warning("Failed to connect to {}:{}".format(host, port))
            return False
        self.local = self.s.getsockname()
        self.remote = self.s.getpeername()
        return True

    def send(self, msg):
        serialized = str.encode(msg+"\n")
        logging.info("Sending Message: " + msg)
        self.s.send(serialized)

    def waitforanswer(self):
        while True:
            recievedbytes = self.s.recv(1024)
            if len(recievedbytes) == 0:
                break
            print(recievedbytes.decode("utf-8"))
            break

    def closeconnection(self):
        self.s.close()
