import json
from threading import Thread
from threading import Timer

from client import myclient


class Tusc(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.servers = [
            {'name': 'local', 'host': "127.0.0.1", 'port': 8443}
        ]
        self.client = myclient.MyClient()

    def run(self):
        if not self.connecttoserver():
            print("Could not connect to a Server, closing...")
            exit()
        self.hello()
        self.heartbeat()

    def connecttoserver(self):
        for idx, server in enumerate(self.servers):
            if self.client.connect(server['host'], server['port']):
                print("Connected to {}".format(server['name']))
                return True
            elif len(self.servers) - 1:
                return False

    def hello(self):
        hello = json.dumps({'type': "hello", 'content': [{'id': self.client.id, 'info': self.client.info}]})
        self.client.send(hello)
        self.client.waitforanswer()

    def heartbeat(self):
        Timer(30.0, self.heartbeat).start()
        beat = json.dumps({'type': "beat"})
        self.client.send(beat)

    def update(self):
        print("todo")

    def upgrade(self):
        print("todo")


if __name__ == "__main__":
    tusc = Tusc()
    tusc.start()
