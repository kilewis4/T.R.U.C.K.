import math
import threading
import time

from WebpageScript import WebpageScript
from TruckGraphic import TruckGraphic
from UnloaderGraphic import UnloaderGraphic
from TruckGraphic import TruckGraphic
from PushNoti import PushNoti
from multiprocessing import Process
# from TruckEntry import app


"""
Method to simulate the "unloading" itself. When a truck is unloaded,
it is removed from the list. Prints the PO number of the truck, the time
the truck was finished unloading, and the time taken. Also unloades the 
eid of the unloader.
"""
def unloading(gui):

    while gui.unloaders.isEmpty():
        yield gui.env.timeout(1)
    print("Unloader found")
    unloader = gui.unloaders.removeUnloader()
    
    truck = gui.trucks.removeTruck()

    time_taken = (truck.size / unloader.pph) * 60

    local_min = 1000
    
    while not gui.doors.openDoors():
        yield gui.env.timeout(1)
    
    for door in gui.doors:
        if door.truck_and_unloader == ():
            if door.pallets < local_min:
                chosen_door = door

    pusher = PushNoti("https://api.pushover.net/1/messages.json", unloader.deviceName, chosen_door.number)
    pusher.send_message()
    
    chosen_unloader_graphic = None
    for unloader_graphic in gui.unloader_graphics:
        if unloader_graphic.eid == unloader.eid:
            unloader_graphic.current_door = chosen_door.number
            chosen_unloader_graphic = unloader_graphic

    start_time = str(gui.env.now)
    gui.add_text('The unloader ' + str(unloader.eid) + ' is unloading truck ' + str(truck.po) + ' at time ' + start_time + " at door: " + str(chosen_door.number))
    chosen_door.assign_job(truck, unloader)
    
    truck_graphic = TruckGraphic(chosen_door.number, truck.po)
    gui.add_truck_graphic(truck_graphic)

    yield gui.env.timeout(time_taken)

    finish_time = str(math.ceil(gui.env.now))

    # webpage_thread = threading.Thread(target= WebpageScript.truck_entry,args=(truck, unloader, start_time, finish_time), daemon=True)
    # webpage_thread.start()

    
    threading.Thread(target = submitter.truck_entry,args=(truck, unloader, start_time, finish_time), daemon=True)

    truck_graphic.done = True
    chosen_unloader_graphic.is_done = True
    chosen_unloader_graphic.current_door = -1
    gui.add_text('Unloader ' + str(unloader.eid) + ' has finished w/truck ' + str(truck.po) + " at " + str(math.ceil(gui.env.now)))
    

    chosen_door.finish_job()
    gui.unloaders.addUnloader(unloader)
    
submitter = WebpageScript()