class Client:
    def __init__(self, ipaddr, date, hostname):
        """

        :param ipaddr: Ip-address of client
        :param date:  First Login
        :param hostname: name of client
        """
        self.name = hostname
        self.ip = ipaddr
        self.lastseen = date
        self.initiallogin = date
        self.info = None

    def printinfo(self):
        """
        Print Information of Client
        :return:
        """
        if self.info:
            print(self.info)
        else:
            print("No Info available")
