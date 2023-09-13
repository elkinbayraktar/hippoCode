import seaborn as sns
import matplotlib.pyplot as plt
from dtypes import unit
import numpy as np
from dtypes import unitPopulation

def plot_ACGs(units : unitPopulation, ax = None, window_size_in = 50,binsize_in = 0.5):
    #first step is to calculate the ccg between them
    for u in units:
        u.calc_unit_ACG(u.spike_times, u.spike_times, window_size = window_size_in, binsize = binsize_in)
    if ax == None:
        fig, ax = plt.subplots(1,1)
    
    numBins = int(window_size_in / binsize_in * 2)
    binLocs = np.linspace(0,1,numBins)
    for u in units:
        ax.bar(x = binLocs, height = u.ACG, width = 1 / (numBins - 1))
        #ax.set_x_ticks(np.arange(-1*window_size_in, window_size_in + binsize_in,binsize_in))
    return ax
    
    
    





