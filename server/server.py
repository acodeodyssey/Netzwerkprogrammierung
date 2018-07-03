import json
import socket

# create new socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
host = 'localhost'
clients = []
# bind to localhost/port
s.bind((host, 8443))

# listen on socket
s.listen(socket.SOMAXCONN)

print("Start server at {}:{}".format(host, 80))

try:
    while True:
        inSocket, addr = s.accept()
        print("Connection from {}".format(addr))
        while True:
            recievedbytes = inSocket.recv(1024)
            if (len(recievedbytes) == 0):
                break
            recievedmsg = recievedbytes.decode("utf-8")
            data = json.loads(recievedmsg)
            print(data['info'])

        inSocket.close()

finally:
    s.close()
