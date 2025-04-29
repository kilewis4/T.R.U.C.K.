import math
import threading
import time
import os
import sys
import json
import random

from WebpageScript import WebpageScript
from datetime import datetime

from pathlib import Path
from TruckGraphic import TruckGraphic
from PushNoti import PushNoti
from multiprocessing import Process

def unloading(env, unloaders, trucks, doors, over_live_wait_time):
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
    while unloaders.isEmpty():
        yield env.timeout(1)

    # Get an available unloader and the next truck in queue
    unloader = unloaders.removeUnloader()
    truck = trucks.removeTruck()

    # Construct the file path for the unloader's historical data
    def resource_path(relative_path):
        try:
            base_path = sys._MEIPASS
        except AttributeError:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)

    file_location = resource_path(f"Data/Unloader_{unloader.eid}.json")

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
    else:
        time_taken = (truck.size / unloader.pph) * 60 # Convert to minutes

    # Look for an available door with the least pallet load
    local_min = 1000
    while not doors.openDoors():
        yield env.timeout(1)
    
    for door in doors:
        if door.truck_and_unloader == ():   # Door is unassigned
            if door.pallets < local_min:
                local_min = door.pallets
                chosen_door = door

    # Send a push notification to the unloader's device
    pusher = PushNoti("https://api.pushover.net/1/messages.json", unloader.deviceName, chosen_door.number)
    pusher.send_message()


    # Log the unloading start in the GUI
    start_time = str(env.now)
    print('The unloader ' + str(unloader.eid) + ' is unloading truck ' + str(truck.po) + ' at time ' + start_time + " at door: " + str(chosen_door.number))
    
    # Assign the truck and unloader to the door
    chosen_door.assign_job(truck, unloader)
    chosen_door.unloading = True
    
    # Add a visual representation of the truck to the GUI

    # Simulate the unloading delay
    yield env.timeout(time_taken)

    # Mark unloading completion time
    finish_time = str(math.ceil(env.now))

    if truck.live == 1 and int(start_time) - int(truck.time) > 120:
        over_live_wait_time[0] += 1

    # Log unloading completion in the GUI
    print('Unloader ' + str(unloader.eid) + ' has finished w/truck ' + str(truck.po) + " at " + str(math.ceil(env.now)))
    chosen_door.unloading = False

    # Mark the door as available again
    chosen_door.finish_job()

    # Return the unloader to the list
    unloaders.addUnloader(unloader)

def get_runtime_dir():
        if getattr(sys, 'frozen', False):  # we're in a PyInstaller bundle
            return Path(sys.executable).parent
        else:
            return Path(__file__).parent.resolve()
    
# Create a single chrome instance when this method is imported
session_timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
csv_file = get_runtime_dir() / f"output_{session_timestamp}.csv"

web = WebpageScript(csv_file)