import simpy
from Truck import Truck
from ProofingProcess import unloading
from ProofingProcessA import unloadingA
from TruckList import TruckList
from TruckListA import TruckListA
from UnloaderList import UnloaderList
from DoorList import DoorList
from DataVisualizerA import visualize

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
    Truck(5, 60, 0, 0, 'Vendor A'),
    Truck(6, 60, 0, 0, 'Vendor A'),
    Truck(7, 60, 0, 0, 'Vendor A'),
    Truck(8, 60, 1, 0, 'Vendor B'),
    Truck(9, 60, 0, 0, 'Vendor A'),
    Truck(10, 60, 0, 0, 'Vendor A'),
    Truck(11, 60, 0, 0, 'Vendor A'),
    Truck(12, 60, 1, 0, 'Vendor B'),
]

for each_truck in test_trucks:
    truck_list_one.addTruck(each_truck, enviroment_one)
    truck_list_two.addTruckA(each_truck, enviroment_two)

print("Our algorithm:")
for each_truck in test_trucks:
    enviroment_one.process(
        unloading(enviroment_one, unloaders_one, truck_list_one, doors_one, baseline_one))
    
enviroment_one.run()

print("FIFO algorithm:")
for each_truck in test_trucks:
    enviroment_two.process(unloadingA(enviroment_two, unloaders_two, truck_list_two, doors_two, baseline_two))

enviroment_two.run()

print("\nThese results print the amount of times a live load stays over 2 hours using our algorithm compared to a FIFO algorithm.")
print("There are 6 trucks total, with 3 live loads\n")

print("Live loads staying over 2 shours with our algorithm: " + str(baseline_one[0]))
print("Live loads staying over 2 hours with FIFO algorithm: " + str(baseline_two[0]) + "\n\n\n\n\n")

visualize()