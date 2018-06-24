import uuid
import socket
import sys
import platform
import ruamel.yaml


class ClientInfo:
    yaml_tag = u'!clientInfo'

    def __init__(self, machine, system, distro):
        self.machine = machine
        self.system = system
        self.distro = distro

    @classmethod
    def to_yaml(cls, representer, node):
        return representer.represent_scalar(cls.yaml_tag,
                                            u'{.machine}-\
                                            {.system}-\
                                            {.distro}'.format(node,
                                                              node,
                                                              node))

    @classmethod
    def from_yaml(cls, constructor, node):
        return cls(*node.value.split('-'))


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
        self.id = uuid.uuid1()
        yaml = ruamel.yaml.YAML()
        yaml.register_class(ClientInfo)
        self.info = yaml.dump([ClientInfo(platform.machine(),
                               platform.system(),
                               platform.linux_distribution())], sys.stdout)

    def connect(self, host, port):
        self.s.connect((host, port))
        self.local = self.s.getsockname()
        self.remote = self.s.getpeername()

    def send(self):
        cmd = None
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
        self.s.close()


def main():
    client = MyClient()
    client.connect(client.host, client.port)
    client.send()
    client.receive()


if __name__ == "__main__":
    main()
