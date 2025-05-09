from Truck import Truck
from UnloadingProcess import unloading
from TruckList import TruckList
from UnloaderList import UnloaderList
from DoorList import DoorList
<<<<<<< HEAD
<<<<<<<< HEAD:Simulation_Legacy/Main.py
========
from multiprocessing import Process
import graphics
>>>>>>>> main:src/Main.py
=======
from multiprocessing import Process
import graphics
>>>>>>> main

import simpy
import threading
import time


env = simpy.RealtimeEnvironment()
incomingTrucks = []
trucks = TruckList(env)
unloaders = UnloaderList(env)
doors = DoorList()

"""
Main method to run all code. Currently makes the truck and employee
list, initializes the enviorment, and prints enviorment time.
"""
def __main__():
    env.process(process_manager(env, incomingTrucks, trucks, unloaders, doors))
    sim_thread = threading.Thread(target=run_simulation, daemon=True)
    sim_thread.start()

<<<<<<< HEAD
=======
    anim_thread = threading.Thread(target=run_animation, daemon=True)
    anim_thread.start()

>>>>>>> main

    program_running = True
    while program_running:
        user_input = input("Press enter when truck arrives, or enter 'quit' to exit.\n")

        if user_input.lower() == 'quit':
            program_running = False
        else:
            add_truck(env, get_truck_data())
            time.sleep(2)
        
    print('The end time is: ' + str(env.now))

""" 
Gathers input from keyboard
Gets input from keyboard and returns a truck object consisting of given parameters.
"""
def get_truck_data():
    po = input("Enter PO#: ")
    size = int(input("Total pallets: "))
    live = 1 if input("Live load (y/n): ") == 'y' else 0
    truck = Truck(po, size, live, env.now)
    return truck

""" 
Runs simulation
Prints the start time and than runs the global enviroment.
"""
def run_simulation():
    print('The start time is: ' + str(env.now))
    env.run()

<<<<<<< HEAD
<<<<<<<< HEAD:Simulation_Legacy/Main.py
""" Manages the incoming trucks being processed
    When new truck arrives adds it to the simulation and begins process.
========
=======
>>>>>>> main


def run_animation(doors):
    door_nums = []
    for door in doors:
        door_nums.append(door.number)
    graphics.animation(door_nums)

""" 
Manages the incoming trucks being processed
When new truck arrives adds it to the simulation and begins process.
<<<<<<< HEAD
>>>>>>>> main:src/Main.py
=======
>>>>>>> main
"""
def process_manager(env, incomingTrucks, trucks, unloaders, doors):
    #Constantly checks for new processes while keeping the simulation running
    while True:
        if incomingTrucks:
            nextTruck = incomingTrucks.pop(0)
            print(str(nextTruck.po) + " has arrived at " + str(nextTruck.time) + " size: " + str(nextTruck.size) + " env time: " + str(env.now))
            trucks.addTruck(nextTruck, env)
            env.process(unloading(env, unloaders=unloaders, trucks=trucks, doors=doors))
        yield env.timeout(1)

""" 
Adds truck
Adds inputted truck to incoming trucks list.
"""
def add_truck(env, truck):
    incomingTrucks.append(truck)

"""
Run the code.
"""
if __name__ == __main__():
    #flask_process = Process(target=start_flask)
    #flask_process.start()
    __main__()
