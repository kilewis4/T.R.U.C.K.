from simpy import Environment
from Truck import Truck
from Unloader import Unloader
from UnloadingProcess import unloading
import random


def __main__():
    env = Environment()

    truck1 = Truck(1, 100)

    unloader1 = Unloader(env, 1, 10)
    unloader2 = Unloader(env, 2, 10)
    unloader3 = Unloader(env, 3, 10)

    unloaders = [Unloader(env, 1, 10),Unloader(env, 2, 10),Unloader(env, 3, 10)]
    trucks = []


    for i in range(100):
        env.process(unloading(env, unloader=unloaders[i % 3], truck=Truck(i, random.randint(0, 100))))

    
    print('The current time is: ' + str(env.now))
    env.run()
    print('The current time is: ' + str(env.now))

if __name__ == __main__():
    __main__()
