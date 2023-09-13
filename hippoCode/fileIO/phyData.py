import matplotlib 
import numpy as np
from pathlib import Path
import pandas as pd

class phyData : 
    def __init__(self,path_in : Path):
        self.fs = None
        self.spike_times = None
        self.spike_clust = None
        self.spike_amp = None 
        self.spike_templates = None
        self.template_shapes = None
        self.templates_ind = None
        self.clusterInfo = None
        self.path = path_in
        self.channel_map = None
        self.process_files()
        self.params = None
        '''Provide more file functionality/attributes/files later on'''

    #Phy Data must be in a folder named phy_files at the level of the working directory
    def process_files(self):
        phyDir = 'phy_files'
        self.spike_times = np.load(self.path /'spike_times.npy' )
        self.spike_clust = np.load(self.path / 'spike_clusters.npy')
        self.spike_amp = np.load(self.path / 'amplitudes.npy')
        self.spike_templates = np.load(self.path / 'spike_templates.npy')
        self.template_shapes = np.load(self.path / 'templates.npy')
        self.clusterInfo = pd.read_csv(self.path / 'cluster_info.tsv', sep = "\t")
        self.channel_map = np.load(self.path / 'channel_map.npy')


        