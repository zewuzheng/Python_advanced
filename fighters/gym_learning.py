import time
# import numpy and gamma
import numpy as np
import matplotlib.pyplot as plt

# Using gamma() method
gfg = np.random.gamma(1)
x = np.linspace(-10,10)

plt.plot(x, gfg)
plt.show()