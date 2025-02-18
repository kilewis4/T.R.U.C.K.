from simpy import Environment
from Truck import Truck
from Unloader import Unloader
from UnloadingProcess import unloading
import random
from TruckList import TruckList
import csv_reader


def __main__():
    


    trucks = TruckList()

    start_truck = trucks.removeTruck()

    env = Environment()

    trucks.addTruck(start_truck)


    unloaders = [Unloader(env, 1, 10),Unloader(env, 2, 10),Unloader(env, 3, 10)]

    env.process(process_generator(env, trucks, unloaders))

    
    print('The current time is: ' + str(env.now))
    env.run()
    
    print('The current time is: ' + str(env.now))

def process_generator(env, trucks, unloaders):
    i = 0

    for t in trucks:
        yield env.timeout(t[1].time)

        env.process(unloading(env, unloader=unloaders[i % 3], trucks= trucks))
        i += 1

if __name__ == __main__():
    __main__()
