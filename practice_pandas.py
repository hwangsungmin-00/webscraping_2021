import numpy as np
import matplotlib.pyplot as plt

x = np.arange(0, 5)     # [0 1 2 3 4]
y = x ** 2              # [ 0  1  4  9 16]

plt.plot(x, y)
plt.show()