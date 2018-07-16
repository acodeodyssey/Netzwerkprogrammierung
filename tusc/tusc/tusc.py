import json
import os
import sys
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
        hello = json.dumps({'type': "hello", 'id': self.client.id, 'info': self.client.info})
        self.client.send(hello)
        self.client.waitforanswer()

    def heartbeat(self):
        Timer(30.0, self.heartbeat).start()
        beat = json.dumps({'type': "beat"})
        self.client.send(beat)

    def update(self, package):
        updatemsg = json.dumps({'type': "update", 'package': package})
        self.client.send(updatemsg)
        self.client.recvpkgs()
        print("finished updating")

    def upgrade(self):
        upgrademsg = json.dumps({'type': "upgrade"})
        self.client.send(upgrademsg)
        self.client.recvpkgs()
        print("finished upgrading")

    def exit(self):
        self.client.closeconnection()
        sys.exit()


if __name__ == "__main__":
    tusc = Tusc()
    tusc.start()
    while True:
        cmd = input().split()
        if cmd[0] == "update" and len(cmd) == 2:
            tusc.update(cmd[1])

        elif cmd[0] == "upgrade":
            tusc.upgrade()

        elif cmd[0] == "quit":
            print("quitting")
            tusc.exit()
            os._exit()

        else:
            print("Not a valid Command, for more info read the Readme")
