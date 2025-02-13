from Truck import Truck
import heapq
import csv_reader

class TruckList:
    def __init__(self):
        self.list = []
            
        trucks = csv_reader.getTrucks()
        for truck in trucks:
            self.addTruck(truck)

    def addTruck(self, truck):
        priorityNumber = -(int (truck.live) * (truck.time * 0.083))
        heapq.heappush(self.list, (priorityNumber, truck))

    def removeTruck(self):
        return heapq.heappop(self.list)[1]

truck1 = TruckList()
truck1.removeTruck()
    
