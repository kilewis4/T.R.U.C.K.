import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.ticker import MultipleLocator

def visualize():
    data = pd.read_csv('output.csv')

    data['unload_duration'] = data['unload_end_time'] - data['unload_start_time']

    for index, row in data.iterrows():
        jitter = np.random.uniform(-0.05, 0.05)
        plt.hlines(row['door'] + jitter, 
                xmin=row["unload_start_time"], 
                xmax=row["unload_end_time"],       
                colors='blue')
        
        colors = ['red', 'blue', 'yellow' 'green']
        plt.plot(row['recieved_time'], row['door'] + jitter, 'X', color=colors[index % 3])
        plt.plot(row["unload_start_time"], row['door'] + jitter, 'o', color=colors[index % 3])
        print(row['door'])
    


    ax = plt.gca()
    ax.yaxis.set_major_locator(MultipleLocator(1))

    fig = plt.gcf()
    fig.autofmt_xdate()
    
    plt.ylim(0, 4)
    plt.tight_layout()

    ax.callbacks.connect('ylim_changed', limit_y_zoom)
    plt.show()

def limit_y_zoom(event_ax):
    ymin, ymax = event_ax.get_ylim()

    if ymin < 0 or ymax > 4:
        new_ymin = max(ymin, 0)
        new_ymax = min(ymax, 4)
        event_ax.set_ylim(new_ymin, new_ymax)
        event_ax.figure.canvas.draw_idle()

