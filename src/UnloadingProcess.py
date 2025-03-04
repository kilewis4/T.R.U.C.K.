import math
import WebpageScript
import threading
import time

"""
Method to simulate the "unloading" itself. When a truck is unloaded,
it is removed from the list. Prints the PO number of the truck, the time
the truck was finished unloading, and the time taken. Also unloades the 
eid of the unloader.
"""
def unloading(env, unloaders, trucks, doors):

    while unloaders.isEmpty():
        yield env.timeout(1)
    print("Unloader found")
    unloader = unloaders.removeUnloader()

    truck = trucks.removeTruck()

    time_taken = (truck.size / unloader.pph) * 60

    local_min = 1000
    
    while not doors.openDoors():
        yield env.timeout(1)
    
    for door in doors:
        if door.truck_and_unloader == ():
            if door.pallets < local_min:
                chosen_door = door
    
    start_time = str(env.now)
    print('The unloader ' + str(unloader.eid) + ' is unloading truck ' + str(truck.po) + ' at ' + start_time + " at door: " + str(chosen_door.number))
    chosen_door.assign_job(truck, unloader)

    yield env.timeout(time_taken)

    finish_time = str(math.ceil(env.now))
    webpage_thread = threading.Thread(target= WebpageScript.truck_entry,args=(truck, unloader, start_time, finish_time), daemon=True)
    webpage_thread.start()
    print('Unloader ' + str(unloader.eid) + ' has finished w/truck ' + str(truck.po) + " at " + str(math.ceil(env.now)))
    chosen_door.finish_job()
    unloaders.addUnloader(unloader)
    
    
    
