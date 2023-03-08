import serial
import matplotlib.pyplot as plt


def plot():
    # connect to Arduino
    ser1 = serial.Serial("/dev/cu.SLAB_USBtoUART", 9600)
    ser1.close()
    ser1.open()

    ser2 = serial.Serial("/dev/cu.SLAB_USBtoUART5", 9600)
    ser2.close()
    ser2.open()

    # create plot
    plt.ion()
    fig = plt.figure()
    xdata = []
    ydata = []

    i = 0

    while True:
        # read data from serial port
        data1 = ser1.readline()
        dumbbell = float(data1.decode())
        print(dumbbell)

        data2 = ser2.readline()
        belt = float(data2.decode())
        # print(belt)

        # append data to plotting array
        xdata.append(i)
        ydata.append(dumbbell)

        # dumbbell value of -1 represents tilting about the y-axis
        # prompt user to straighten wrist
        if dumbbell < 0:
            print("Please straighten wrist.")
        else:
            plt.scatter(i, dumbbell)
        i += 1

        # belt value of 1 represents tilting to the left (y > 10)
        # belt value of -1 represents tilting to the right (y < -10)
        if belt > 0:
            print("You are tilting to the left. Please correct your form.")
        elif belt < 0:
            print("You are tilting to the right. Please correct your form.")
        # plot update rate
        plt.show()
        plt.pause(0.001)


plot()
