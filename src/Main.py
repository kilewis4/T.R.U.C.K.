from simpy import Environment
from Truck import Truck
from Unloader import Unloader
from UnloadingProcess import unloading
import random
from TruckList import TruckList
import csv_reader


def __main__():
    env = Environment()


    trucks = TruckList()


    unloaders = [Unloader(env, 1, 10),Unloader(env, 2, 10),Unloader(env, 3, 10)]

    for i in range(100):
        env.process(unloading(env, unloader=unloaders[i % 3], truck= trucks.removeTruck()))

    
    print('The current time is: ' + str(env.now))
    env.run()
    print('The current time is: ' + str(env.now))

if __name__ == __main__():
    __main__()
