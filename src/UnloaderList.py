from Unloader import Unloader
import csv_reader

class UnloaderList:
    def __init__(self, env):
        self.list = []
        self.env = env

        unloaders = csv_reader.getUnloaders(env)
        for unloader in unloaders:
            self.addUnloader(unloader)


    def addUnloader(self, unloader):
        self.list.append(unloader)

    def removeUnloader(self):
        return self.list.pop()[1]
    
    def getSize(self):
        return self.list.__len__()