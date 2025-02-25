from Truck import Truck
import csv_reader


"""
Trucklist contains a list of all the trucks that come in in a day.
It has several methods to manage the truck, including __iter__,
addTruck, removeTruck, and getSize.
"""
class TruckList:
    """
    Creates a TruckList object, and inserts all of the data from
    csv_reader into the list of trucks.
    """
    def __init__(self):
        self.list = []
            
        trucks = csv_reader.getTrucks()
        for truck in trucks:
            self.addTruck(truck)
    
    """
    Returns an iterator for the list itself.

    Returns:
        The iterator to the list.
    """
    def __iter__(self):
        return iter(self.list)
        

    """
    Calculates the priority number of a truck based on its arrival time
    and if its live or not. Appends this truck into the list, and sorts
    the list.

    Args:
        truck(Truck): Truck to add
    """
    def addTruck(self, truck):
        priorityNumber = -(int (truck.live) * (truck.time * 0.083))
        self.list.append((priorityNumber, truck))
        self.list.sort()

    """
    Removes a truck at the front of the list and returns it.

    Returns:
        The truck that was removed.
    """
    def removeTruck(self):
        return self.list.pop(0)[1]
    
    """
    Gets the current size of the list of trucks.

    Returns:
        The size of the list.
    """
    def getSize(self):
        return self.list.__len__()
    