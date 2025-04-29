class TruckListA:
    """
    A class that manages a list of trucks for a specific day, including adding, 
    removing, and getting the size of the truck list. It also calculates the 
    priority of each truck based on its arrival time and whether it's live.

    Attributes:
        list (list): A list of trucks in the truck list, where each truck is paired
                     with its calculated priority.
        env (object): The environment object used to determine the current time.

    Methods:
        __iter__(): Returns an iterator for the list of trucks.
        addTruck(truck, env): Adds a truck to the list with a calculated priority and sorts the list.
        removeTruck(): Removes the truck at the front of the list and returns it.
        getSize(): Returns the current size of the truck list.
    """
    
    def __init__(self, env):
        """
        Initializes the TruckList with an empty list and the given environment.

        Args:
            env (object): The environment object used to track time in the simulation.
        """
        self.list = []
        self.env = env

    def __iter__(self):
        """
        Returns an iterator for the truck list.

        Returns:
            iterator: An iterator object for the list of trucks.
        """
        return iter(self.list)

    def addTruckA(self, truck, env):
        """
        Adds a truck to the list with a priority based on its arrival time and live status.
        The truck is added to the list, and the list is then sorted.

        Args:
            truck (Truck): The truck to add to the list.
            env (object): The environment object used to calculate the truck's priority.
        """
        self.list.append((0, truck))

    def removeTruckA(self):
        """
        Removes and returns the truck at the front of the list.

        Returns:
            Truck: The truck that was removed from the list.
        """
        result = self.list.pop(0)[1]

        return result

    def getSize(self):
        """
        Gets the current size of the truck list.

        Returns:
            int: The size of the truck list.
        """
        return len(self.list)
