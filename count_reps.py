import matplotlib.pyplot as plt
from scipy.signal import find_peaks
import numpy as np
from scipy.signal import lfilter
import serial
from datetime import datetime

exercises = {1: 'Reverse Fly', 2: 'Side-Lying External Rotation', 3: 'Arm Flexion', 4: 'Lying Arm Abduction'}
data = [10,0,0,0,0,0,0,-2,-2,-2,-2,-2,-2,1,2,3,3,4,5,6,7,8,9,10,10,10,9,10,9,8,8,7,6,6,7,8,9,10,9,9,8,7,7,6,5,3,2,2,1,1,1,2,3,2,4,5,5,6,6,7,6,5,4,3,2,1.5,1]
data = [i * 9 for i in data]


def start(reps, sets, exercise, date):
    # connect to Arduino
    # ser1 = serial.Serial("/dev/cu.SLAB_USBtoUART7", 9600)
    # ser1.close()
    # ser1.open()
    #
    # ser2 = serial.Serial("/dev/cu.SLAB_USBtoUART", 9600)
    # ser2.close()
    # ser2.open()

    # create plot
    plt.ion()
    # fig = plt.figure()
    xdata = []
    ydata = []
    i = 0
    j = 0

    n = 3  # smoothness of curve
    b = [1.0 / n] * n
    a = 1
    threshold = 20
    diff = 30
    set = 1
    rep = 0
    calibrated = False
    prev = -10
    plt.pause(1)

    while set <= sets:
        # read data from serial port
        # data1 = ser1.readline()
        # dumbbell = float(data1.decode())

        # data2 = ser2.readline()
        # belt = float(data2.decode())
        dumbbell = data[j]
        print(dumbbell)

        # dumbbell value of -2 represents calibration
        if prev == -18 and dumbbell != -18:
            calibrated = True
        elif dumbbell == -18:
            print('Calibrating')
            calibrated = False
            plt.title('Set ' + str(set) + '/' + str(sets) + ' of ' + str(reps) + ' Repetitions of ' + exercises[exercise] + ' Exercise')
            plt.xlabel('Time (ms)')
            plt.ylabel('Angle (degrees)')
        prev = dumbbell

        # record data values
        if calibrated:
            # append data to plotting array
            xdata.append(i)
            ydata.append(dumbbell)
            y = lfilter(b, a, ydata)
            series_y = np.array(y)
            series_f = np.array(y)
            peaks, _ = find_peaks(series_f)
            mins, _ = find_peaks(series_f * -1)
            rep = len(peaks)
            x = np.linspace(0, len(xdata), len(series_f))  # figure out what these parameters mean

            # dumbbell value of -1 represents tilting about the y-axis
            # prompt user to straighten wrist
            if dumbbell == -1:
                print("Please straighten wrist.")
            else:
                plt.plot(xdata, ydata, color='black', label='raw data')  # raw dumbbell data
                # plt.plot(xdata, y, color='blue', label='filtered data')  # filtered dumbbell data
                # plt.plot(x[mins], series_f[mins], 'x', label='mins')
                # plt.plot(x[peaks], series_f[peaks], '*', label='peaks')
            i += 1

            # # belt value of 1 represents tilting to the left (y > 10)
            # if belt > 0:
            #     print("You are tilting to the left. Please correct your form.")
            # # belt value of -1 represents tilting to the right (y < -10)
            # elif belt < 0:
            #     print("You are tilting to the right. Please correct your form.")
            # plot update rate
            # plt.xlim(i - 100, i)
            plt.show()
            plt.pause(0.001)

        # if the number of rps has been completed, save the graph
        if rep == reps and dumbbell < threshold:
            i = 0
            rep = 0
            xdata = []
            ydata = []
            plt.savefig('graphs/' + date + '_' + str(set) + '.png')
            set += 1
            calibrated = False
        j += 1
    # print(peaks)
    while True:
        a = 1


start(3, 2, 1, 'filename')