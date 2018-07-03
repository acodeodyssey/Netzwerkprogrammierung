from client import myclient
import json

host = "127.0.0.1"
port = 8443
client = myclient.myclient()
client.connect(host, port)
client.send(json.dumps({'id': client.id, 'info': client.info}))
