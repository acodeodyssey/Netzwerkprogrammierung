class Client:
    def __init__(self, ipaddr, date, hostname):
        self.name = hostname
        self.ip = ipaddr
        self.lastseen = date
        self.initiallogin = date
        self.info = None

    def printinfo(self):
        if self.info:
            print(self.info)
        else:
            print("No Info available")
