from simpy import Environment
from Truck import Truck
from Unloader import Unloader
from UnloadingProcess import unloading
import random
from TruckList import TruckList
import csv_reader
from UnloaderList import UnloaderList

"""
Main method to run all code. Currently makes the truck and employee
list, initializes the enviorment, and prints enviorment time.
"""
def __main__():
    trucks = TruckList()
    start_truck = trucks.removeTruck()
    env = Environment()
    trucks.addTruck(start_truck)
    unloaders = UnloaderList(env)
    env.process(process_generator(env, trucks, unloaders.list))
    
    print('The current time is: ' + str(env.now))
    env.run()
    print('The current time is: ' + str(env.now))

"""
Method to process the trucks with the unloaders, assigining the trucks to the unloaders.

Args:
    env (Environment): enviorment which is used to process.
    trucks (list): list of trucks that need to be unloaded.
    unloaders (list): unloaders that will unload the trucks.
"""
def process_generator(env, trucks, unloaders):
    i = 0
    for t in trucks:
        yield env.timeout(t[1].time)
        env.process(unloading(env, unloader=unloaders[i % 3], trucks=trucks))
        i += 1

"""
Run the code.
"""
if __name__ == __main__():
    __main__()
