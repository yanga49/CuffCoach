import matplotlib.pyplot as plt
from scipy.signal import find_peaks
import numpy as np
from scipy.signal import lfilter
import serial
from datetime import datetime
import time

# exercises to select from
translator = {'american-football.png': 1, 'bars.png': 2, 'weightlifting.png': 3, 'athletics.png': 4}
exercises = {1: 'Reverse Fly', 2: 'Side-Lying External Rotation', 3: 'Arm Flexion', 4: 'Lying Arm Abduction'}

'''
The Plotter class allows users to automatically track their physiotherapy workouts and save results and data.
    - Begin each set by pressing the button on the device
    - Set is terminated automatically when number of reps has been reached or when max time is exceeded
    - At the end of each set, a graph of the ROM data is saved to the graphs folder
    - At the end of all sets, the total number of successful and failed reps are saved to the data folder
'''


class Plotter:
    def __init__(self, repetitions: int, sets: int, exercise: str, weight: int, goalROM: float):
        # initialize exercise variables
        self.reps = repetitions
        self.sets = sets
        self.exercise = exercises[translator[exercise]]
        self.max_time = 7 * repetitions
        # initialize name/title variables
        self.filename = 'data/exercise_' + str(translator[exercise]) + '.txt'
        self.weight = weight
        # initialize filtering variables
        self.n = 5  # smoothness of filtered curve
        self.b = [1.0 / self.n] * self.n
        self.a = 1
        # initialize progress tracking variables
        self.goalROM = goalROM - self.n  # adjust target based on filter value
        self.date = str(datetime.today())[:10]
        self.success = 0
        self.fail = 0

        # print(self.reps, self.sets, self.exercise, self.weight, self.goalROM)

    # write() function writes the date, weight, successful reps, and failed reps to a data file
    def write(self):
        f = open(self.filename, "a")
        f.write(self.date + ',' + str(self.weight) + ',' + str(self.success) + ',' + str(self.fail) + '\n')
        f.close()

    # plot() function plots a real-time graph of the exercise and saves the graph as a png
    def plot(self):
        # connect to Arduino
        ser1 = serial.Serial("/dev/cu.SLAB_USBtoUART", 9600)
        ser1.close()
        ser1.open()
        ser2 = serial.Serial("/dev/cu.SLAB_USBtoUART7", 9600)
        ser2.close()
        ser2.open()

        # create plot and initialize x-variables
        plt.ion()
        xdata = []
        ydata = []
        i = 0
        j = 0

        # initialize rep/set count variables
        threshold = 10
        set = 1
        rep = 0

        # initialize calibration variables
        calibrated = False
        prev = -10
        plt.pause(1)

        # initialize filtered data arrays
        series_f = []
        peaks = []

        start = None

        # continue loop until all sets are completed
        while set <= self.sets:
            # read dumbbell data from serial port
            data1 = ser1.readline()
            dumbbell = float(data1.decode())
            # print(dumbbell)

            # read belt data from serial port
            data2 = ser2.readline()
            belt = float(data2.decode())

            # CALIBRATION CODE
            # if just finished calibrating, take start time
            if prev == -2 and dumbbell != -2 and dumbbell != -3:
                calibrated = True
                start = time.time()
            # dumbbell value of -2 represents calibrating
            elif dumbbell == -2:
                print('Calibrating')
                calibrated = False
                plt.title('Set ' + str(set) + '/' + str(self.sets) + ' of ' + str(self.reps) + ' Repetitions of ' +
                          self.exercise + ' Exercise (' + str(self.weight) + 'lbs)')
                plt.xlabel('Time (ms)')
                plt.ylabel('Angle (degrees)')
                plt.axhline(y=self.goalROM, color='green', linestyle='dashed')
            # dumbbell value of -3 represents pre-calibration
            elif dumbbell == -3:
                print('Calibrating in 5 seconds.')
            # dumbbell value of -4 represents uncalibrated gyroscope
            elif dumbbell == -4:
                print('To calibrate dumbbell gyroscope, place the sensor on a flat surface.')
            # dumbbell value of -5 represents button pressed
            elif dumbbell == -5:
                print('Begin next set.')
            # if dumbbell is not calibrated, prompt user to press button
            elif not calibrated:
                print('To begin the next set, press the button.')
            # keep track of previous value to determine start/end of calibration
            prev = dumbbell

            # DATA COLLECTION CODE
            if calibrated:
                # dumbbell value of -1 represents tilting about the y-axis
                if dumbbell == -1:
                    # prompt user to straighten wrist, don't plot values
                    print("Please straighten wrist.")
                else:
                    print("Good form! Keep it up!")
                    # append data to plotting array
                    xdata.append(i)
                    ydata.append(dumbbell)
                    # filter data to find local maxima and keep track of reps
                    y = lfilter(self.b, self.a, ydata)
                    series_f = np.array(y)
                    # number of peaks = the number of reps
                    peaks, _ = find_peaks(series_f)
                    mins, _ = find_peaks(series_f * -1)
                    rep = len(peaks)
                    x = np.linspace(0, len(xdata), len(series_f))
                    plt.plot(xdata, ydata, color='black', label='raw data')  # raw dumbbell data
                    # plt.plot(x[peaks], series_f[peaks], 'x')  # peaks
                    # plt.plot(xdata, y, color='blue', label='filtered data')  # filtered dumbbell data

                    # belt value of 1 represents tilting to the left (y > 10)
                    if self.exercise == 'Reverse Fly':
                        if belt == 1:
                            print("You are tilting to the left. Please correct your form.")
                            plt.scatter(i, ydata[i], color='blue')
                        # belt value of -1 represents tilting to the right (y < -10)
                        elif belt == -1:
                            print("You are tilting to the right. Please correct your form.")
                            plt.scatter(i, ydata[i], color='red')
                        # belt value of -2 represents uncalibrated gyroscope
                        elif belt == -2:
                            print("To calibrate belt gyroscope, place the sensor on a flat surface.")

                    i += 1

                # plot update rate
                plt.show()
                # plt.pause(0.001)

            # take end time to check if max time has elapsed
            end = time.time()
            if start is None:
                pass
            # once the set has been completed (#reps) or max time exceeded,
            # save the graph and reset variables for next set
            elif (rep == self.reps and threshold > dumbbell >= 0) or end - start > self.max_time:
                start = None
                i = 0
                rep = 0
                for peak in series_f[peaks]:
                    print(peak)
                    if peak < self.goalROM:
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
        # append data to progress plot data
        self.write()


# my_plotter = Plotter(3, 2, 1, 10, 70)
# my_plotter.plot()
