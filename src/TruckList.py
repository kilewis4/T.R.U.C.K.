from Truck import Truck
import csv_reader

class TruckList:
    def __init__(self):
        self.list = []
            
        trucks = csv_reader.getTrucks()
        for truck in trucks:
            self.addTruck(truck)
    
    def __iter__(self):
        return iter(self.list)
        

    def addTruck(self, truck):
        priorityNumber = -(int (truck.live) * (truck.time * 0.083))
        self.list.append((priorityNumber, truck))
        self.list.sort()

    def removeTruck(self):
        return self.list.pop()[1]
    
    def getSize(self):
        return self.list.__len__()
    
