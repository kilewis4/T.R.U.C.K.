from Truck import Truck
import heapq


list = []

def addTruck(truck):
    priorityNumber = -(int (truck.live) * (truck.time * 0.083))
    heapq.heappush(list, (priorityNumber, truck))

def removeTruck():
    return heapq.heappop()