import pandas as pd
import datetime
from Truck import Truck


def getTrucks():
    df = pd.read_csv(filepath_or_buffer="./Data/truck_data_02_04_2025.csv", usecols=[7,16,26,41])
    new_list = df.values.tolist()
    print(new_list)


    trucks = []
    for truck in new_list:
        time = truck[1]
        month = int(time[:2])
        day = int(time[3:5])
        year = int(time[6:10])
        hour = int(time[11:13])
        minute = int(time[14:16])
        print(datetime.datetime(year, month, day, hour, minute))
        trucks.append(Truck(int(truck[2]), int (truck[3]), int(truck[0]), ((day * 10000) + (hour * 100) + (minute * 1))))

    return trucks
