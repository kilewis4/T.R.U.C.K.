from simpy import Environment
from Door import Door
from Truck import Truck
from Unloader import Unloader
from UnloadingProcess import unloading
import random
from TruckList import TruckList
import csv_reader


def __main__():
    


    trucks = TruckList()
    

    #start_truck = trucks.removeTruck() -> This is for the reason below.

    env = Environment()

    #trucks.addTruck(start_truck) -> This is for having the enviroment start the time of the first truck.


    unloaders = [Unloader(env, 1, 10),Unloader(env, 2, 10),Unloader(env, 3, 10)]
    doors = [Door(1), Door(2), Door(3)]

    env.process(process_generator(env, trucks, unloaders, doors))


    
    print('The current time is: ' + str(env.now))
    env.run()
    
    print('The current time is: ' + str(env.now))

def process_generator(env, trucks, unloaders, doors):
    i = 0

    for each_truck in trucks:
        index = i % 3
        doors[index].assign_job(each_truck[1], unloader=unloaders[index])
        print(doors[index])
        yield env.timeout(each_truck[1].time)
        doors[index].fill_dock()
        

        env.process(unloading(env, unloader=unloaders[index], trucks= trucks))
        doors[index].finish_job()
        i += 1

if __name__ == __main__():
    __main__()
