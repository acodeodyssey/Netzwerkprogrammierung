import socket
import time


host = 'localhost'
port = 8443

# create new socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)

# bind to localhost/port
s.bind((host, port))

# listen on socket
s.listen(socket.SOMAXCONN)

print("Start server at {}:{}".format(host, port))

try:
    while True:
        inSocket, addr = s.accept()

        print("Connection from {}".format(addr))

        msg = "Hello {0}, nice to meet you!\n".format(*socket.gethostbyaddr
                                                      (addr[0]))
        msg2 = "it's {1}/{2}/{0} {3}:{4}:{5}\n".format(*time.localtime())
        inSocket.send(bytes(msg, 'utf-8'))
        inSocket.send(bytes(msg2, 'utf-8'))
        inSocket.close()

finally:
    s.close()
