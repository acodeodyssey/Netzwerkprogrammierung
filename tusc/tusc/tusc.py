import json

from client import myclient

host = "127.0.0.1"
port = 8443
client = myclient.MyClient()
client.connect(host, port)
hello = json.dumps({'id': client.id, 'info': client.info})
client.send(hello)
