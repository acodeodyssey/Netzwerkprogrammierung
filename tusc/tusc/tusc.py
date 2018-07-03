import json

from client import myclient


class Tusc:
    def __init__(self):
        host = "127.0.0.1"
        port = 8443
        self.client = myclient.MyClient()
        self.client.connect(host, port)

    def hello(self):
        hello = json.dumps({'type': "hello", 'content': [{'id': self.client.id, 'info': self.client.info}]})
        self.client.send(hello)

    def heartbeat(self):
        print("todo")

    def update(self):
        print("todo")

    def upgrade(self):
        print("todo")


if __name__ == "__main__":
    tusc = Tusc()
    tusc.hello()
