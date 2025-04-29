import os
import sys

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from datetime import datetime


from pathlib import Path
from matplotlib.ticker import MultipleLocator

def get_runtime_dir():
        if getattr(sys, 'frozen', False):  # we're in a PyInstaller bundle
            return Path(sys.executable).parent
        else:
            return Path(__file__).parent.resolve()

def visualize():
    #data = pd.read_csv('output.csv')
    # data = pd.read_csv(resource_path('output.csv'))
    session_timestamp = datetime.now().strftime("%Y-%m-%d")
    data = get_runtime_dir() / f"output_{session_timestamp}.csv"
    data = pd.read_csv(data)

    data['unload_duration'] = data['unload_end_time'] - data['unload_start_time']

    plt.close('all')

    for index, row in data.iterrows():
        jitter = np.random.uniform(-0.05, 0.05)
        plt.hlines(row['door'] + jitter, 
                xmin=row["unload_start_time"], 
                xmax=row["unload_end_time"],       
                colors='blue')
        
        colors = ['red', 'blue', 'yellow' 'green']
        plt.plot(row['received_time'], row['door'] + jitter, 'X', color=colors[index % 3])
        plt.plot(row["unload_start_time"], row['door'] + jitter, 'o', color=colors[index % 3])

    

    
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

def resource_path(relative_path):
        try:
            base_path = Path(sys._MEIPASS)
        except AttributeError:
            base_path = Path(__file__).parent.resolve()
        return base_path / relative_path