from simpy import Environment
from Door import Door
from Truck import Truck
from Unloader import Unloader
from UnloadingProcess import unloading
from TruckList import TruckList
from UnloaderList import UnloaderList
from DoorList import DoorList

import random
import csv_reader

"""
Main method to run all code. Currently makes the truck and employee
list, initializes the enviorment, and prints enviorment time.
"""
def __main__():
    trucks = TruckList()

    #start_truck = trucks.removeTruck() -> This is for the reason below

    env = Environment()

    #trucks.addTruck(start_truck) -> This is for having the enviroment start the time of the first truck.


    unloaders = UnloaderList(env)

    # for unloader in unloaders.list:
    #     print(unloader.eid)

    doors = DoorList()

    env.process(process_generator(env, trucks, unloaders, doors))

    
    print('The current time is: ' + str(env.now))
    env.run()
    print('The current time is: ' + str(env.now))

def process_generator(env, trucks, unloaders, doors):
    i = 0

    for each_truck in trucks:
        unloader_index = i % unloaders.getSize()
        door_index = i % doors.getSize()
        #print(index)


        doors.list[door_index].assign_job(each_truck[1], unloader=unloaders.list[unloader_index])
        print(doors.list[door_index])
        
        env.process(unloading(env, unloaders=unloaders, trucks= trucks))
        doors.list[door_index].fill_dock()
        doors.list[door_index].finish_job()

        yield env.timeout(each_truck[1].time)
        
        i += 1

"""
Run the code.
"""
if __name__ == __main__():
    __main__()
