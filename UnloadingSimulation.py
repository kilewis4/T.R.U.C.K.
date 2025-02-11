from simpy import Resource, Environment, Process
import random

class Unloader(Resource):
    def __init__(self, env, eid, pph):
        Resource.__init__(self, env, capacity = 1)
        self.eid = eid
        self.pph = pph

class Truck(object):
    def __init__(self, po, size):
        self.po = po
        self.size = size

def unloading(env, unloader, truck):
    with unloader.request() as req:
        print(str(truck.po) + " has arrived at " + str(env.now))
        yield req

        print('The unloader ' + str(unloader.eid) + ' is unloading truck ' + str(truck.po) + ' at ' + str(env.now))
        yield env.timeout(truck.size / unloader.pph)
        print('Unloader ' + str(unloader.eid) + ' has finished w/truck ' + str(truck.po))


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



