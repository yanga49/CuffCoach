import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

class ProgressPlot:

    def plotprogress(filename, exercisename):
        dates = []
        weights = []
        successes = []
        fails = []
        i = 0
        file = open(filename, 'r')
        for line in file:
            temp = line.rstrip().split(",")
            i += 1
            dates.append(i)
            weights.append(int(temp[1]))
            successes.append(int(temp[2]))
            fails.append(int(temp[3]))
        
        
        bar_width = 0.25

        # Set the positions of the bars on the x-axis
        r1 = np.arange(len(dates))
        r2 = [x + bar_width for x in r1]
        r3 = [x + bar_width for x in r2]

        # Create the figure and axis objects
        fig, ax = plt.subplots()

        # Plot the first set of data
        ax.bar(r1, successes, color='green', width=bar_width, label='Successful reps')

        # Plot the second set of data, stacked on top of the first set
        ax.bar(r2, fails,color='red', width=bar_width, label='Failed reps')

        # Plot the third set of data, grouped with the first two sets
        ax.bar(r3, weights, color='blue', width=bar_width, label='Weight')

        # Set the x-axis labels and ticks
        ax.set_xlabel("Days")
        ax.set_ylabel("Reps", color='blue')
        ax.tick_params(axis='y', labelcolor='blue')
        ax.set_yticks(np.arange(0,max(weights),1))
        ax.legend()

        ax2 = ax.twinx()
        ax2.set_ylabel('Weight', color='red')
        
        ax2.set_yticks(np.arange(0, max(weights), 1))

        plt.title("Progress Chart of " + exercisename)
        plt.show()

    #plotprogress("data/exercise_1.txt", "Reverse Fly")
