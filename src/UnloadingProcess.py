

def unloading(env, unloader, truck):
    with unloader.request() as req:
        print(str(truck.po) + " has arrived at " + str(env.now))
        yield req

        print('The unloader ' + str(unloader.eid) + ' is unloading truck ' + str(truck.po) + ' at ' + str(env.now))
        yield env.timeout(truck.size / unloader.pph)
        print('Unloader ' + str(unloader.eid) + ' has finished w/truck ' + str(truck.po))