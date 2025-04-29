import simpy
from Truck import Truck
from ProofingProcess import unloading
from ProofingProcessA import unloadingA
from TruckList import TruckList
from TruckListA import TruckListA
from UnloaderList import UnloaderList
from DoorList import DoorList
from DataVisualizer import visualize

baseline_one = [0]
baseline_two = [0]

enviroment_one = simpy.Environment(30)
enviroment_two = simpy.Environment(30)

truck_list_one = TruckList(enviroment_one, False)
truck_list_two = TruckListA(enviroment_two)

unloaders_one = UnloaderList(enviroment_one)
unloaders_two = UnloaderList(enviroment_two)

doors_one = DoorList()
doors_two = DoorList()

test_trucks = [
    Truck(1, 60, 0, 0, 'Vendor A'),
    Truck(2, 60, 0, 0, 'Vendor A'),
    Truck(3, 60, 0, 0, 'Vendor A'),
    Truck(4, 60, 1, 0, 'Vendor B'),
]

for each_truck in test_trucks:
    truck_list_one.addTruck(each_truck, enviroment_one)
    truck_list_two.addTruckA(each_truck, enviroment_two)

print("Sim 1:")
for each_truck in test_trucks:
    enviroment_one.process(
        unloading(enviroment_one, unloaders_one, truck_list_one, doors_one, baseline_one))
    
enviroment_one.run()

print("Sim 2:")
for each_truck in test_trucks:
    enviroment_two.process(unloadingA(enviroment_two, unloaders_two, truck_list_two, doors_two, baseline_two))

enviroment_two.run()

print("Sim 1: " + str(baseline_one[0]), "Sim 2: " + str(baseline_two[0]))
