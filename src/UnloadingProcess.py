from TruckList import TruckList

def unloading(env, unloader, trucks):
    
    truck = trucks.removeTruck()
    with unloader.request() as req:
        print(str(truck.po) + " has arrived at " + str(truck.time))
        time_taken = truck.size / unloader.pph
        for each_truck in trucks:
            each_truck[1].time += time_taken
            print(f"each_truck[1].time: {each_truck[1].time}")
        yield req

        print('The unloader ' + str(unloader.eid) + ' is unloading truck ' + str(truck.po) + ' at ' + str(env.now))
        yield env.timeout(time_taken)
        print('Unloader ' + str(unloader.eid) + ' has finished w/truck ' + str(truck.po))
        