from TruckList import TruckList
import math

"""
Method to simulate the "unloading" itself. When a truck is unloaded,
it is removed from the list. Prints the PO number of the truck, the time
the truck was finished unloading, and the time taken. Also unloades the 
eid of the unloader.
"""
def unloading(env, unloaders, trucks):

    while unloaders.isEmpty():
        yield env.timeout(1)
    print("Unloader found")
    unloader = unloaders.removeUnloader()

    truck = trucks.removeTruck()


    # Need to see if this is requesting from the list of just one unloader
    


        
    

    time_taken = (truck.size / unloader.pph) * 60



    print('The unloader ' + str(unloader.eid) + ' is unloading truck ' + str(truck.po) + ' at ' + str(env.now))
    yield env.timeout(time_taken)
    print('Unloader ' + str(unloader.eid) + ' has finished w/truck ' + str(truck.po) + " at " + str(math.ceil(env.now)))
    unloaders.addUnloader(unloader)