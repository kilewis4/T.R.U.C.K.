from queue import Queue

class Truck:
    def __init__(self, po_number, pallets, time_in):
        self.po_number = po_number
        self.pallets = pallets
        self.time_in = time_in

class Associate:
    def __init__(self, name, eid, pph):
        self.name = name
        self.eid = eid
        self.pph = pph

def simulation(trucks, associates):
    truckLine = Queue(len(trucks))
    associatesWaiting = Queue(len(associates))
    associatesWorking = {}


    world_clock = 0

    while world_clock < 2400:

        for truck in trucks:
            if truck.time_in == world_clock:
                truckLine.put(truck)


        if truckLine.empty() == False:
            truck_next = truckLine.get()
            print(truck_next.po_number)

        world_clock += 1

        


trucks = [Truck(1, 10, 100), Truck(2, 10, 200), Truck(3, 10, 2300)]
associates = [Associate("A", 1, 10), Associate("B", 2, 15), Associate("C", 3, 20)]

simulation(trucks=trucks, associates=associates)

        


