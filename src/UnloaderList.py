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
        for unloader in unloaders[1:4]:
            print(unloader.eid)
            self.addUnloader(unloader)
    
    """
    Returns an iterator for the list itself.

    Returns:
        The iterator to the list.
    """
    def __iter__(self):
        return iter(self.list)

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
        return self.list.pop(0)
    
    """
    Gets the size of the unloader list.

    Returns:
        The length of the unloader list.
    """
    def getSize(self):
        return self.list.__len__()
    
    """
    Determines if list of unloaders is empty.
    
    Returns:
        Boolean value of whether the list is empty
    """
    def isEmpty(self):
        return self.getSize() == 0
    

    """
    Gets the current size of the list of unloaders.

    Returns:
        The size of the list.
    """
    def getSize(self):
        return self.list.__len__()