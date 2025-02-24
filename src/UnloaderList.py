from Unloader import Unloader
import csv_reader

"""
Unloader list which initializes the list using csv_reader,
and add the unloaders to the list. Also has the ability to
remove the list and get the size.
"""
class UnloaderList:
    """
    Initiazlises the list, gets the data from csv_reader, 
    and adds the unloaders to the list.

    Args:
        env (Enviorment): enviorment which used for getUnloaders.
    """
    def __init__(self, env):
        self.list = []
        self.env = env
        unloaders = csv_reader.getUnloaders(env)
        for unloader in unloaders:
            self.addUnloader(unloader)

    """
    Appends an unloader to the list.

    Args:
        unloader (Unloader): unloader to be appended
    """
    def addUnloader(self, unloader):
        self.list.append(unloader)

    """
    Removes an unloader to the list.

    Returns:
        The value of the list element removed.
    """
    def removeUnloader(self):
        return self.list.pop()[1]
    
    """
    Gets the size of the unloader list.

    Returns:
        The length of the unloader list.
    """
    def getSize(self):
        return self.list.__len__()