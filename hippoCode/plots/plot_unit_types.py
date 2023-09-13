import seaborn as sns
import matplotlib.pyplot as plt
from dtypes import unit
import numpy as np
from dtypes import unitPopulation
from mpl_toolkits import mplot3d


def plot_unit_clusters(units : unitPopulation, ax = None):

    #check if axes were provided
    if ax == None: 
        fig = plt.figure()
        ax = fig.add_subplot(projection = '3d')
    
    #extract the units which will be plotted
    for u in unitPopulation.units_list:
        if u.type == 'int':
            ax.scatter(u.type_features[2],u.type_features[3], u.type_features[1],color = 'blue', label = 'interneuron')
        #
        elif u.type == 'pyr':
            ax.scatter(u.type_features[2],u.type_features[3], u.type_features[1],color = 'red', label = 'pyramidal')
        #mua or lua - can plot the mua or lua as low brightness gray dots 
        else:
            continue
    ax.set_xlabel('Trough-Peak time')
    ax.set_ylabel('Tau Decay coefficient')
    ax.set_zlabel('Mean ISI')
    ax.legend()