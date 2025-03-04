from Door import Door

"""
Door list which currently is made on arbitrary values. 
Also has the ability to remove the list and get the size.
"""
class DoorList:
    """
    Initiazlises the list, and adds the doors to the list.

    Args:
        env (Enviorment): enviorment which used for getUnloaders.
    """
    def __init__(self):
        self.list = []
        doors = [Door(1), Door(2), Door(3)]
        for door in doors:
            self.addDoor(door)

    """
    Returns an iterator for the list itself.

    Returns:
        The iterator to the list.
    """
    def __iter__(self):
        return iter(self.list)

    """
    Appends an door to the list.

    Args:
        door (Door): door to be appended
    """
    def addDoor(self, door):
        self.list.append(door)

    """
    Removes an door to the list.

    Returns:
        The value of the list element removed.
    """
    def removeDoor(self):
        return self.list.pop(0)
    
    """
    Gets the size of the door list.

    Returns:
        The length of the door list.
    """
    def getSize(self):
        return self.list.__len__()
    
    """
    Determines if list of doors is empty.
    
    Returns:
        Boolean value of whether the list is empty
    """
    def isEmpty(self):
        return self.getSize() == 0
    
    """ Find open door
    Iterates through the list of doors and determines if there exists one without a truck and unloader.

    Returns:
        Boolean value of wether a door is avaliable
    """
    def openDoors(self):
        for door in self.list:
            if door.truck_and_unloader == ():
                return True
        return False
    

    """
    Gets the current size of the list of doors.

    Returns:
        The size of the list.
    """
    def getSize(self):
        return self.list.__len__()