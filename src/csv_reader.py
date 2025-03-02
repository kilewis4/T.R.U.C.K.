import pandas as pd
import datetime
from Truck import Truck
from Unloader import Unloader
import random

"""
Method to extract all of the trucks from the truck data csv.
Also parses through the time variable and reworks it.

Returns: 
    List of trucks extracted from the trucks data csv.
"""
def getTrucks():
    df = pd.read_csv(filepath_or_buffer="./Data/truck_data_02_04_2025.csv", usecols=[7,16,26,41])
    new_list = df.values.tolist()

    trucks = []
    for truck in new_list:
        live = truck[0]
        time = truck[1]
        month = int(time[:2])
        day = int(time[3:5])
        year = int(time[6:10])
        hour = int(time[11:13])
        minute = int(time[14:16])
        time_parsed = (((day * 10000) + (hour * 100) + (minute * 1)) - 40000) % 1200
        trucks.append(Truck(int(truck[2]), int (truck[3]), int(truck[0]), (hour * 100) + (minute * 1)))

    trucks.reverse()



    return trucks[0:5]

"""
Method to extract all of the employees from the employee data csv.
Specificailly, it grabs the employee IDs and generates a random 
value from 25 to 40 as their pallets per hour.

Args:
    env (Environment): enviroment variable passed in so we don't
    make a new process.

Returns:
    List of unloaders extracted.
"""
def getUnloaders(env):
    edf = pd.read_csv(filepath_or_buffer="./Data/employee_data_02_04_2025.csv", usecols=[0])
    new_unloader_list = edf.iloc[:, 0].unique().tolist()    

    unloaders = []
    for unloader in new_unloader_list:
        eid = unloader
        pallets_per_hour = random.randint(25,40)
        unloaders.append(Unloader(env, eid, pallets_per_hour))

    return unloaders



