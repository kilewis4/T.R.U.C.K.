import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

data = pd.read_csv('output.csv')

print(data)
fig, ax = plt.subplots()
for row in data:
    plt.figure()

plt.show()