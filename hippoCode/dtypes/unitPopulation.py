#module imports
from dtypes.unit import unit 
#library imports
import numpy as np 
from fileIO.phyData import phyData
import pandas as pd

class unitPopulation:
    #Constructor - pass in phy spike data for unit info consolidation
    def __init__(self,phy:phyData):
        self.numUnits = None
        self.units_list = None
        self.fs = 30000
        self.process_phy(phy)
        

    def process_phy(self,phy):
        fs = 30000
        uniqueSpikeIDs,inverseInds,spikeCounts = np.unique(ar = phy.spike_clust,return_inverse=True, return_counts=True)
        #create a list of units for holding the spikes
        self.units_list = [unit(phyID_in = uniqueSpikeIDs[i]) for i in range(len(uniqueSpikeIDs))]
        phy_groups = phy.clusterInfo['group'].to_numpy(dtype = str)
        phy_channels = phy.clusterInfo['ch'].to_numpy(dtype = 'int16')
        #loop thru all spikes and their corresponding info --> assign each spike as tuple(t,amp) to correct unit's list of spikes
        for t,amp,u,template in zip(phy.spike_times,phy.spike_amp,inverseInds,phy.spike_templates):
            self.units_list[u].add_spike(t/fs*1000,amp)
            self.units_list[u].add_template(template)
        #sort the spikes in the dictionary based on tieme
        for i , _ in enumerate(self.units_list):
            _.sort_spikes()
            _.find_best_temp_ID()
            _.extract_temp_waveform(phy.template_shapes)
            _.phy_group = phy_groups[i]
            _.phy_channel = phy_channels[i]

    
            














        
    def plot_FRs(self,units,time_window,binsize, mode):

        time_elapsed = time_window[1] - time_window[0]
        '''DATA PREPROCESSING
            - obtain the binned firing rate of units specified
                - loop thru all spikes occurring during the time window of interest'''

        FR_array = np.zeros(len(units),time_elapsed / binsize)
        #loop over the units specified 
        for u in units:
            #find the first occurrence of a spike within the desired range
            firstSpike = np.where(self.units_dict[u][0] >= time_window[0])
            #loop thru unit's spikes: start from the first spike in the time window, break upon reaching end of time_window
            for i in range(firstSpike,len(self.units_dict[u])):
                if(self.units_dict[u][i][0] >= time_window[1]):
                    break
                binNum = np.floor((self.units_dict[u][i][0] - time_window[0]) / binsize)
                #add to tally of spikes within time bin for this unit(u)
                FR_array[u][binNum] += 1
        
        if mode == 'line':
            from matplotlib.pyplot import eventplot

    def get_cell_types(self): 
        for u in self.units_list:
            u.get_cell_type()


    


