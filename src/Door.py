from simpy import Container

"""
Door class at which a truck would park.
"""
class Door(Container):
    """
    Initializes the door number, also contains num of pallets and a tuple
    that contain the unloader and truck that is at the door.

    Args:
        number(int): Door number to uniquely identify it
    """
    def __init__(self, number):
        self.number = number
        self.truck_and_unloader = ()
        self.pallets = 0

    """
    Prints the door number along with the truck and employee number.

    Returns:
        The print statement containing the door number, truck number, and employee number.
    """
    def __repr__(self):
        return "Door " + str(self.number) + " with (" + str(self.truck_and_unloader[0].po) + ", " +  str(self.truck_and_unloader[1].eid) + ")"
    
    """
    Puts a truck and unloader in the object tuple.

    Args:
        truck(Truck): Truck to be put in first part of tuple
        unloader(Unloader): Unloader to be put in first part of tuple
    """
    def assign_job(self, truck, unloader):
        self.truck_and_unloader = (truck, unloader)

    """
    Empty the tuple, indicating that the unloading has been finished.
    """
    def finish_job(self):
        self.fill_dock()
        self.truck_and_unloader = ()
        
    
    """
    Put the number of pallets in the truck into the palets variable.
    """
    def fill_dock(self):
        self.pallets = self.truck_and_unloader[0].size
