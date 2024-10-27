import numpy as np
import matplotlib.pyplot as plt
import os
from scipy.optimize import curve_fit

os.chdir(os.path.abspath(os.path.dirname(__file__)))

bins, count = [], []
with open("hist2.csv", "r") as f:
    for line in f.readlines():
        _b, _c = [float(i) for i in line.split(",")]
        bins.append(_b)
        count.append(_c)


def two_gaussians(x, a1, b1, c1, a2, b2, c2):
    return (a1 * np.exp(-((x - b1) ** 2) / (2 * c1 ** 2)) +
            a2 * np.exp(-((x - b2) ** 2) / (2 * c2 ** 2)))

def fit_two_gaussians(bins, count):
    initial_guess = [max(count) / 2, bins[np.argmax(count)], 1,
                     max(count) / 2, bins[np.argmax(count) + 5], 1]
    
    params, covariance = curve_fit(two_gaussians, bins, count, p0=initial_guess)
    
    return params


params = fit_two_gaussians(bins, count)

a1, b1, c1, a2, b2, c2 = params
print(f"Gaussian 1: Amplitude: {a1}, Mean: {b1}, Stddev: {c1}")
print(f"Gaussian 2: Amplitude: {a2}, Mean: {b2}, Stddev: {c2}")

gaussian1 = a1 * np.exp(-((np.array(bins) - b1) ** 2) / (2 * c1 ** 2))
gaussian2 = a2 * np.exp(-((np.array(bins) - b2) ** 2) / (2 * c2 ** 2))

plt.scatter(bins, count, label='Data', s=5)
plt.plot(bins, gaussian1, color='blue', linestyle='dashed', label='Gaussian 1')
plt.plot(bins, gaussian2, color='green', linestyle='dashed', label='Gaussian 2')
plt.title('Individual Gaussian Fits to Data')
plt.xlabel('Bins')
plt.ylabel('Count')
plt.legend()
plt.show()


integral1 = np.trapz(gaussian1, bins)
integral2 = np.trapz(gaussian2, bins)


total_integral = integral1 + integral2

ratio1 = integral1 / total_integral if total_integral != 0 else 0
ratio2 = integral2 / total_integral if total_integral != 0 else 0

print(f"Integral of Gaussian 1: {integral1}")
print(f"Integral of Gaussian 2: {integral2}")
print(f"Ratio of Gaussian 1 to Total: {ratio1}")
print(f"Ratio of Gaussian 2 to Total: {ratio2}")
