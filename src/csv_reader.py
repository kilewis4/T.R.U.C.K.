import pandas as pd
from Truck import Truck


def getTrucks():
    df = pd.read_csv(filepath_or_buffer="./Data/truck_data_02_04_2025.csv", usecols=[7,26,41])
    new_list = df.values.tolist()
    #print(new_list)

    trucks = []
    for truck in new_list:
        trucks.append(Truck(int(truck[1]), int (truck[2]), int(truck[0]), 0))

    return trucks

list = getTrucks()
for t in list:
    print(t.live)
