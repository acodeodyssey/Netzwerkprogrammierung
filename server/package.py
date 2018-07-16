class Package:
    """
    Package holds information about package
    """
    def __init__(self, pname, pversion, purl, pfile):
        """

        :param pname:  Name of package
        :param pversion: Version of package
        :param purl: url of package
        :param pfile: file path
        """
        self.name = pname
        self.version = pversion
        self.url = purl
        self.file = pfile

