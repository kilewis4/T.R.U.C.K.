import simpy
from Door import Door
from Truck import Truck
from Unloader import Unloader
from UnloadingProcess import unloading
from TruckList import TruckList
from UnloaderList import UnloaderList
from DoorList import DoorList

import random
import csv_reader
import threading
import time


env = simpy.RealtimeEnvironment(initial_time=320)
incomingTrucks = []
trucks = TruckList(env)
unloaders = UnloaderList(env)
doors = DoorList()

"""
Main method to run all code. Currently makes the truck and employee
list, initializes the enviorment, and prints enviorment time.
"""
def __main__():
    
    csv_reader.getTrucks()
        
    

    #start_truck = trucks.removeTruck() -> This is for the reason below

    #trucks.addTruck(start_truck) -> This is for having the enviroment start the time of the first truck.


    

    # for unloader in unloaders.list:
    #     print(unloader.eid)

    

    env.process(process_manager(env, incomingTrucks, trucks, unloaders, doors))
    sim_thread = threading.Thread(target=run_simulation, daemon=True)
    sim_thread.start()
    
    for truck in csv_reader.getTrucks():
        if env.now < truck.time - 1:
            time.sleep(truck.time - env.now - 1)
        add_truck(env, truck)

    time.sleep(200)


    

    print('The end time is: ' + str(env.now))

""" Runs simulation
    Prints the start time and than runs the global enviroment.
"""
def run_simulation():
    print('The start time is: ' + str(env.now))
    env.run()

def process_manager(env, incomingTrucks, trucks, unloaders, doors):
    """Constantly checks for new processes while keeping the simulation running"""
    while True:
        if incomingTrucks:
            nextTruck = incomingTrucks.pop(0)
            print(str(nextTruck.po) + " has arrived at " + str(nextTruck.time) + " size: " + str(nextTruck.size) + " env time: " + str(env.now))
            trucks.addTruck(nextTruck, env)
            env.process(unloading(env, unloaders=unloaders, trucks= trucks))
        yield env.timeout(1)

def add_truck(env, truck):
    incomingTrucks.append(truck)

""" This is legacy code for generating processes based on a single list of trucks.
def process_generator(env, trucks, unloaders, doors):
    i = 0

    for each_truck in trucks:
        print("inside process_generator")
        unloader_index = i % unloaders.getSize()
        door_index = i % doors.getSize()
        #print(index)

        yield env.timeout(each_truck[1].time)


        doors.list[door_index].assign_job(each_truck[1], unloader=unloaders.list[unloader_index])
        print(doors.list[door_index])
        
        env.process(unloading(env, unloaders=unloaders, trucks= trucks))
        doors.list[door_index].fill_dock()
        doors.list[door_index].finish_job()

        
        
        i += 1
"""

"""
Run the code.
"""
if __name__ == __main__():
    __main__()
