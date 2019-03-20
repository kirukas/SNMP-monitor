class Device:
    def __init__(self,ip,port,community):
        self.ip = ip
        self.port = port
        self.community = community
        self.syso = None
        self.location = None
        self.contact = None
    def setIP(self,ip):
        self.ip = ip
    def setPort(self,p):
        self.port = p
    def setCommunity(self, c):
        self.community = c
    def setSyso(self, s):
        self.syso = s
    def setLocation(self,l):
        self.location = l
    def setContac(self, c):
        self.contact = c
    def getIP(self):
        return self.ip
    def getPort(self):
        return self.port
    def getCommunity(self):
        return self.community
    def getSyso(self):
        return self.syso
   
