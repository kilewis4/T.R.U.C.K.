class Door:
    def __init__(self, number, truck_and_unloader, pallets):
        self.number = number
        self.truck_and_unloader = truck_and_unloader
        self.pallets = pallets
    
    def assign_job(self, truck, unloader):
        self.truck_and_unloader = (truck, unloader)
    
    def fill_dock(self):
        self.pallets = self.truck_and_unloader[0].size

