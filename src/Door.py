from simpy import Container

class Door(Container):
    def __init__(self, number):
        self.number = number
        self.truck_and_unloader = ()
        self.pallets = 0

    def __repr__(self):
        return "Door " + str(self.number) + " with (" + str(self.truck_and_unloader[0].po) + " , " +  str(self.truck_and_unloader[1].eid) + ")"
    
    def assign_job(self, truck, unloader):
        self.truck_and_unloader = (truck, unloader)

    def finish_job(self):
        self.truck_and_unloader = ()
    
    def fill_dock(self):
        self.pallets = self.truck_and_unloader[0].size

