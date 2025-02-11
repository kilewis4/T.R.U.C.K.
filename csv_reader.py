import pandas as pd
from UnloadingSimulation import Truck

df = pd.read_csv(filepath_or_buffer="./Data/truck_data_02_04_2025.csv", usecols=[26,41])
new_list = df.values.tolist()
#print(new_list)

trucks = []
for truck in new_list:
    trucks.append(Truck(int(truck[0]), truck[1]))

for truck in trucks:
    print(truck.size)