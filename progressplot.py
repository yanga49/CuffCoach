import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

class ProgressPlot:

    def plotprogress(filename):
        dates = []
        weights = []
        successes = []
        fails = []
        file = open(filename, 'r')
        for line in file:
            temp = line.rstrip().split(",")
            dates.append(temp[0])
            weights.append(int(temp[1]))
            successes.append(temp[2])
            fails.append(temp[3])
        
        
        bar_width = 0.25

        # Set the positions of the bars on the x-axis
        r1 = np.arange(len(dates))
        r2 = [x + bar_width for x in r1]
        r3 = [x + bar_width for x in r2]

        # Create the figure and axis objects
        fig, ax = plt.subplots()

        # Plot the first set of data
        ax.bar(r1, successes, color='blue', width=bar_width, label='Data 1')

        # Plot the second set of data, stacked on top of the first set
        ax.bar(r1, fails, bottom=successes, color='red', width=bar_width, label='Data 2')

        # Plot the third set of data, grouped with the first two sets
        ax.bar(r2, weights, color='green', width=bar_width, label='Data 3')

        # Set the x-axis labels and ticks
        ax.set_xticks([r + bar_width for r in range(len(dates))])
        ax.set_xticklabels(dates)

        # Set the axis labels and legend
        ax.set_xlabel('Category')
        ax.set_ylabel('Value')
        ax.legend()
    
        plt.xlabel("Days")
        plt.ylabel("Weight")
        plt.title(filename)
        plt.legend()
        plt.show()      
        print(successes)
    plotprogress("data/exercise_1.txt")
