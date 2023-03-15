import matplotlib.pyplot as plt
from scipy.signal import find_peaks
import numpy as np
from scipy.signal import lfilter

n = 3  # the larger n is, the smoother curve will be
b = [1.0 / n] * n
a = 1
y = [7,6,5,4,3,2,1,1.00001,1,1,2,2,3,5,6,9,9,10,11,12,12,12,13,13,12, 12, 12,11,10,8,6,3,5,6,7,8,13,15,11,12,9,6,4,8,9,10,15,16,17,19,22,17,15,13,11,10,7,5,8,9,12]
yy = lfilter(b, a, y)
#plt.plot(x, yy, linewidth=2, linestyle="-", c="b")
series = np.array(yy)
peaks, _ = find_peaks(series)
mins, _ = find_peaks(series * -1)
t_lower = 30
x = np.linspace(0, 10, len(series))
plt.plot(x, series, color='black')
plt.plot(x[mins], series[mins], 'x', label='mins')
plt.plot(x[peaks], series[peaks], '*', label='peaks')
plt.plot(x, y, color='green')
plt.plot(x, yy, color='red')
plt.legend()
print(series[peaks])
print(series[mins])
plt.show()
