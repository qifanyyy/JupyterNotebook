import os
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Based on https://github.com/CoreyMSchafer/code_snippets/blob/master/Python/Matplotlib/09-LiveData/finished_code.py

class ProgressVisualizer():

    def __init__(self, data_file):
        self.data_file = data_file

    def visualize(self):        
        plt.style.use('fivethirtyeight')

        def animate(i):            

            if not os.path.isfile(self.data_file):
                return

            data = pd.read_csv(self.data_file)
            iteration = data['iteration']
            maximum = data['max']
            minimum = data['min']
            mean = data['mean']
            std = data['std']

            plt.cla()

            plt.plot(iteration, maximum, label='maximum', linewidth=2)
            plt.plot(iteration, minimum, label='minimum', linewidth=2)
            plt.plot(iteration, mean, label='mean', linewidth=2)
            plt.plot(iteration, mean + std, label='mean + std', linewidth=2)
            plt.plot(iteration, mean - std, label='mean - std', linewidth=2)

            
            plt.legend(loc='upper left')
            plt.tight_layout()

        ani = FuncAnimation(plt.gcf(), animate, interval=1000)

        plt.tight_layout()
        plt.show()