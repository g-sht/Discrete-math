import numpy as np
from hassediagram import plot_hasse

data = (np.array([
    [0, 1, 1, 1, 0,0,0,0],
    [0, 0, 0, 0, 1,1,0,0],
    [0, 0, 0, 0, 1,0,1,0],
    [0, 0, 0, 0, 0,1,1,0],
    [0, 0, 0, 0, 0,0,0,1],
    [0, 0, 0, 0, 0,0,0,1],
    [0, 0, 0, 0, 0,0,0,1],
    [0, 0, 0, 0, 0,0,0,0],

]))

plot_hasse(data)