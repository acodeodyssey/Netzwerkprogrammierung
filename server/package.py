class Package:
    def __init__(self, pname, pversion, purl, pfile):
        self.name = pname
        self.version = pversion
        self.url = purl
        self.file = pfile

    def createChecksum(self):
        print("todo")
