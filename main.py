import os
import sys

import matplotlib
matplotlib.use("Qt5Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import pypsa

n = pypsa.Network("networks/WP2024_north-west.nc")


print(n.buses.to_string())
#n.plot(bus_sizes=0.0025, margin=0.25)
#plt.show()
