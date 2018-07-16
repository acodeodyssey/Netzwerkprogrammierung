import json
import logging
import platform
import socket
import uuid


class MyClient:
    def __init__(self, s=None):
        """
        Initialize Client to communicate with server
        and create information about the client
        :param s: socket of client
        """
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
        """
        Connect to Server
        :param host: server host
        :param port: server port
        :return:
        """
        try:
            self.s.connect((host, port))
        except socket.error:
            logging.warning("Failed to connect to {}:{}".format(host, port))
            return False
        self.local = self.s.getsockname()
        self.remote = self.s.getpeername()
        return True

    def send(self, msg):
        """
        Send message to server
        :param msg: message to be send
        :return:
        """
        serialized = str.encode(msg+"\n")
        logging.info("Sending Message: " + msg)
        self.s.send(serialized)

    def recvpkgs(self):
        """
        First part of Communication: Information about the Package
        Second part: the file
        then loop until all packages are updated
        :return:
        """
        while True:
            while True:
                recievedbytes = self.s.recv(1024)
                if len(recievedbytes) == 0:
                    break
                break

            pkginfo = json.loads(recievedbytes)
            name = pkginfo['file']
            if name == "endTransfer":
                break
            print("updating:{}".format(name))
            f = open(name, 'wb')

            while True:
                l = self.s.recv(1024)
                if len(l) == 0:
                    f.close()
                    break
                f.write(l)
                break
            f.close()

    def waitforanswer(self):
        """
        Wait for an answer of server
        :return:
        """
        while True:
            recievedbytes = self.s.recv(1024)
            if len(recievedbytes) == 0:
                break
            print(recievedbytes.decode("utf-8"))
            break

    def closeconnection(self):
        """
        Close the connection
        :return:
        """
        self.s.close()
