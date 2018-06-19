import uuid
import socket
import sys
import os


host = sys.argv[1]
port = int(sys.argv[2])
cmd = None
# create info based on os, todo gpu,cpu etc und struct
osinfo = os.uname()
# create id based on host ID and current time
id = uuid.uuid1()
if len(sys.argv) >= 4:
    cmd = sys.argv[3]

# create new socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)

# connect to host:port
s.connect((host, port))

# get information about connection
local = s.getsockname()
remote = s.getpeername()

print("{}:{} -> {}:{}".format(local[0], local[1], remote[0], remote[1]))

# send cmd
if cmd is not None:
    # convert cmd into byte array
    sentbytes = s.send(bytes(cmd+"\n", 'utf-8'))

# recieve response
while True:
    recievedbytes = s.recv(10)
    if (len(recievedbytes) == 0):
        break
    print(recievedbytes.decode('utf-8'))

# close connection
s.close()
