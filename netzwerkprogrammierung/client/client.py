import platform
import uuid
import socket
import sys
import json


class MyClient:
    def __init__(self, s=None):
        # initialize socket
        if s is None:
            self.s = socket.socket(socket.AF_INET,
                                   socket.SOCK_STREAM,
                                   socket.IPPROTO_TCP)
        else:
            self.s = s
        self.host = sys.argv[1]
        self.port = int(sys.argv[2])
        self.id = str(uuid.uuid1())
        self.info = {'machine': platform.machine()}

    def _connect(self, host, port):
        self.s.connect((host, port))
        self.local = self.s.getsockname()
        self.remote = self.s.getpeername()

    def _send(self, msg):
        try:
            serialized = str.encode(msg+"\n")
        except (TypeError, ValueError):
            raise Exception('You can only send JSON-serializable data')
        print("Sending Message: " + msg)
        self.s.send(serialized)
        self.s.close()


def main():
    client = MyClient()
    client._connect(client.host, client.port)
    client._send(json.dumps(client.info))


if __name__ == "__main__":
    main()
