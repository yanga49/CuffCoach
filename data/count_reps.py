import matplotlib.pyplot as plt
from scipy.signal import find_peaks
import numpy as np
from scipy.signal import lfilter
import serial
from datetime import datetime

# Exercises to select from
exercises = {1: 'Reverse Fly', 2: 'Side-Lying External Rotation', 3: 'Arm Flexion', 4: 'Lying Arm Abduction'}


# The plotter class allows users to automatically track their physiotherapy workouts and save results and data.
class Plotter:
    def __init__(self, repetitions, sets, exercise, weight):
        self.reps = repetitions
        self.sets = sets
        self.exercise = exercises[exercise]
        self.filename = 'exercise_' + str(exercise) + '.txt'
        self.weight = weight
        self.date = str(datetime.today())[:10]
        self.success = 0
        self.fail = 0

    # Function that writes the date, weight, successful reps, and failed reps to a text file
    def write(self):
        f = open(self.filename, "a")
        f.write(self.date + ',' + str(self.weight) + ',' + str(self.success) + ',' + str(self.fail) + '\n')
        f.close()

    # Function that plots a real-time graph of the exercise and saves the graph as a png
    def plot(self):
        # connect to Arduino
        ser1 = serial.Serial("/dev/cu.SLAB_USBtoUART", 9600)
        ser1.close()
        ser1.open()
        # ser2 = serial.Serial("/dev/cu.SLAB_USBtoUART", 9600)
        # ser2.close()
        # ser2.open()

        # create plot
        plt.ion()
        xdata = []
        ydata = []
        i = 0
        j = 0

        n = 5  # smoothness of curve
        b = [1.0 / n] * n
        a = 1

        threshold = 10
        set = 1
        rep = 0

        calibrated = False
        prev = -10
        full = 70
        plt.pause(1)

        series_f = []
        peaks = []

        while set <= self.sets:
            # read data from serial port
            data1 = ser1.readline()
            if data1[0] == 141 or data1[2] == 241:  # ignore initializing output
                dumbbell = -5
            else:
                dumbbell = float(data1.decode())

            # data2 = ser2.readline()
            # belt = float(data2.decode())
            # dumbbell = data[j]
            # print(dumbbell)

            if prev == -2 and dumbbell != -2 and dumbbell != -3:
                calibrated = True
            elif dumbbell == -2:
                print('Calibrating')
                calibrated = False
                plt.title('Set ' + str(set) + '/' + str(self.sets) + ' of ' + str(self.reps) + ' Repetitions of ' +
                          self.exercise + ' Exercise (' + str(self.weight) + 'lbs)')
                plt.xlabel('Time (ms)')
                plt.ylabel('Angle (degrees)')
            elif dumbbell == -3:
                print('Calibrating in 5 seconds')
            elif dumbbell == -4:
                print('To calibrate the gyroscope, place the sensor on a flat surface.')
            elif dumbbell == -5:
                print('Initializing...')
            else:
                print(dumbbell)
            prev = dumbbell

            # record data values
            if calibrated:
                # append data to plotting array
                xdata.append(i)
                ydata.append(dumbbell)
                # filter data to find local maxima
                y = lfilter(b, a, ydata)
                series_f = np.array(y)
                # the number of peaks = the number of reps
                peaks, _ = find_peaks(series_f)
                mins, _ = find_peaks(series_f * -1)
                rep = len(peaks)
                x = np.linspace(0, len(xdata), len(series_f))

                # dumbbell value of -1 represents tilting about the y-axis
                # prompt user to straighten wrist
                if dumbbell == -1:
                    print("Please straighten wrist.")
                else:
                    plt.plot(xdata, ydata, color='black', label='raw data')  # raw dumbbell data
                    # plt.plot(x[peaks], series_f[peaks], 'x')  # peaks
                    # plt.plot(xdata, y, color='blue', label='filtered data')  # filtered dumbbell data
                i += 1

                # # belt value of 1 represents tilting to the left (y > 10)
                # if belt > 0:
                #     print("You are tilting to the left. Please correct your form.")
                # # belt value of -1 represents tilting to the right (y < -10)
                # elif belt < 0:
                #     print("You are tilting to the right. Please correct your form.")

                # plot update rate
                plt.show()
                plt.pause(0.001)

            # if the number of reps has been completed, save the graph and reset for next set
            if rep == self.reps and dumbbell < threshold:
                i = 0
                rep = 0
                for peak in series_f[peaks]:
                    print(peak)
                    if peak < full:
                        self.fail += 1
                    else:
                        self.success += 1
                xdata = []
                ydata = []
                plt.savefig('graphs/' + self.date + '_' + str(set) + '.png')
                plt.cla()
                set += 1
                calibrated = False
            j += 1
        self.write()


my_plotter = Plotter(3, 2, 1, 10)
my_plotter.plot()
