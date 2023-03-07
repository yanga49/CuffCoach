import serial
import matplotlib.pyplot as plt

# connect to Arduino
ser = serial.Serial("/dev/cu.SLAB_USBtoUART", 9600)
ser.close()
ser.open()

# create plot
plt.ion()
fig = plt.figure()
xdata = []
ydata = []

i = 0

while True:
    # read data from serial port
    data = ser.readline()
    temp = float(data.decode())
    print(temp)
    # append data to plotting array
    xdata.append(i)
    ydata.append(temp)
    # angle of -1 represents tilting about the y-axis
    # prompt user to straighten wrist
    if temp < 0:
        print("Please straighten wrist.")
    else:
        plt.scatter(i, temp)
    i += 1
    # plot update rate
    plt.show()
    plt.pause(0.0001)
