import math
import threading
import time
import os
import sys

from WebpageScript import WebpageScript

import json
import random
from pathlib import Path
from TruckGraphic import TruckGraphic
from UnloaderGraphic import UnloaderGraphic
from TruckGraphic import TruckGraphic
from PushNoti import PushNoti
from multiprocessing import Process

def unloading(gui):
    """
    Coroutine to simulate the unloading of a truck by an available unloader.

    This function performs the following:
    - Waits until at least one unloader is available.
    - Selects a truck and unloader.
    - Attempts to estimate the unloading time based on historical data.
    - Finds the optimal dock door with minimal pallet load.
    - Notifies the unloader via a push notification.
    - Assigns the truck and unloader to a dock.
    - Simulates the unloading duration.
    - Updates the GUI and backend with unloading status.
    - Re-adds the unloader back into the available pool.

    Args:
        gui: A GUI controller object that manages the simulation environment,
             unloader and truck pools, doors, and visual updates.
    """

    # Wait until there is at least one available unloader
    while gui.unloaders.isEmpty():
        yield gui.env.timeout(1)
    print("Unloader found")

    # Get an available unloader and the next truck in queue
    unloader = gui.unloaders.removeUnloader()
    truck = gui.trucks.removeTruck()

    # Construct the file path for the unloader's historical data
    def resource_path(relative_path):
        try:
            base_path = sys._MEIPASS
        except AttributeError:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)

    path = Path("Data") / f"Unloader_{unloader.eid}.json"
    file_location = Path(resource_path(path.as_posix()))
    #file_location = path.resolve()

    potential_times = []
    # Attempt to find a realistic unload time from past data
    with open(file_location, "r") as file:
        loaded_data = json.load(file)
        for each_row in loaded_data:
            if each_row.get("Main_Vendor_Name") == truck.vendor:   
                if  int (each_row.get("Total_Pallet_Finished_Count")) >= truck.size - 5 and int (each_row.get("Total_Pallet_Finished_Count")) <= truck.size + 5:
                    potential_times.append(each_row.get("Total_Time_In_Minutes"))
    
    # Use historical time if available; otherwise, calculate manually
    if (len(potential_times) != 0):
        time_taken = int (potential_times[random.randint(0, len(potential_times) - 1)])
        print(time_taken)
    else:
        time_taken = (truck.size / unloader.pph) * 60 # Convert to minutes
        print(str (time_taken) + " else")

    # Look for an available door with the least pallet load
    local_min = 1000
    while not gui.doors.openDoors():
        yield gui.env.timeout(1)
    
    for door in gui.doors:
        if door.truck_and_unloader == ():   # Door is unassigned
            if door.pallets < local_min:
                chosen_door = door

    # Send a push notification to the unloader's device
    pusher = PushNoti("https://api.pushover.net/1/messages.json", unloader.deviceName, chosen_door.number)
    pusher.send_message()
    
    chosen_unloader_graphic = None
    for unloader_graphic in gui.unloader_graphics:
        if unloader_graphic.eid == unloader.eid:
            unloader_graphic.current_door = chosen_door.number
            chosen_unloader_graphic = unloader_graphic

    # Log the unloading start in the GUI
    start_time = str(gui.env.now)
    gui.add_text('The unloader ' + str(unloader.eid) + ' is unloading truck ' + str(truck.po) + ' at time ' + start_time + " at door: " + str(chosen_door.number))
    
    # Assign the truck and unloader to the door
    chosen_door.assign_job(truck, unloader)
    chosen_door.unloading = True
    
    # Add a visual representation of the truck to the GUI
    truck_graphic = TruckGraphic(chosen_door.number, truck.po)
    gui.add_truck_graphic(truck_graphic)

    # Simulate the unloading delay
    yield gui.env.timeout(time_taken)

    # Mark unloading completion time
    finish_time = str(math.ceil(gui.env.now))
    webpage_thread = threading.Thread(target= web.truck_entry,args=(truck, unloader, chosen_door, start_time, finish_time), daemon=True)

    webpage_thread.start()

    # Update the graphics to reflect completion
    truck_graphic.done = True
    chosen_unloader_graphic.is_done = True
    chosen_unloader_graphic.current_door = -1

    # Log unloading completion in the GUI
    gui.add_text('Unloader ' + str(unloader.eid) + ' has finished w/truck ' + str(truck.po) + " at " + str(math.ceil(gui.env.now)))
    chosen_door.unloading = False

    # Mark the door as available again
    chosen_door.finish_job()

    # Return the unloader to the list
    gui.unloaders.addUnloader(unloader)
    
# Create a single chrome instance when this method is imported
web = WebpageScript()