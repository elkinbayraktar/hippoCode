import matplotlib.pyplot as plt
import numpy as np 
from scipy.optimize import curve_fit

class unit: 
    def __init__(self,phyID_in):
        self.spike_times = []
        self.spike_amps = []
        self._ACG = None
        self.spike_template_IDs = []
        self.best_template_ID = None
        self._waveform = None
        self.bestChan = None
        self._t_trough_peak = None
        self._peakVoltage = None
        self.type = None
        self.type_features = None
        self._phyID = None
        self.phy_group = None
        self.phy_channel = None
        self.fs = 30000


    @property
    def phyID(self,ID):
        return self.phyID
    
    def add_spike(self,t, amp):
        self.spike_times.append(t)
        self.spike_amps.append(amp)
    
    def add_template(self,temp):
        self.spike_template_IDs.append(temp)
    
    #find the best template ID for this unit
    '''May Add averaging of the most relevant spike templates'''
    def find_best_temp_ID(self):
        #return the unique tempIDs and the counts of each template for this unit
        uniqueTemps, uniqueCounts = np.unique(self.spike_template_IDs, return_counts= True)
        #the best template is the template which most spikes for this unit corresponded to 
        max_template = uniqueTemps[np.argmax(uniqueCounts)]
        self.best_template_ID = max_template
    
    #extract the waveform shape of the template from the template_arr using (original template #, : , bestChannel)
    def extract_temp_waveform(self,template_arr):
        self.find_best_temp_ID()
        #extract 2d array of only this templates shapes on all channels 
        temp_shapes = template_arr[self.best_template_ID][:][:]
        #extract the channel with the max template waveform
        temp_bestChan = np.unravel_index(np.argmin(temp_shapes),shape = np.shape(temp_shapes))[1]
        #extract the waveform given best template ID and channel for this unit
        self._waveform = temp_shapes[:,temp_bestChan]

    def sort_spikes(self):
        sorted_times = []
        sorted_amps = []
        spike_order_inds = np.argsort(self.spike_times)
        for i in range(len(self.spike_times)):
            sorted_times.append(self.spike_times[spike_order_inds[i]])
            sorted_amps.append(self.spike_amps[spike_order_inds[i]])
        self.spike_times = np.array(sorted_times)
        self.spike_amps = np.array(sorted_amps)


    def calc_unit_ACG(self,spikesRef, spikesTarget, window_size = 50, binsize = .5):
        self.ACG = np.zeros(int(window_size / binsize * 2 ))
        window_size_arr = np.ones(len(spikesTarget)) * window_size
        #left indices are the indices where a spike with t = t - 150 would go 
        left_indices = np.searchsorted(spikesRef,spikesTarget - window_size_arr, side = 'left')
        #right_indices are the indices where a spike with t = t + 150 would go
        right_indices = np.searchsorted(spikesRef,spikesTarget + window_size_arr, side = 'left')
        #now need to increment bin value in self.acg
        numBins = len(self.ACG)
        if numBins % 2 == 0:
            midBinLeft = numBins / 2 - 1
            midBinRight = numBins / 2  
        #case of odd number of bins
        else:
            midBin = numBins // 2
        
        #loop thru all target spikes and corresponding intervals of interest in ref spikes
        for targetSpike, left_ind, right_ind in zip(spikesTarget, left_indices, right_indices):
            #loop thru the interval of interest for this reference spike
            for s in range(left_ind,right_ind):
                #calc time of target spike relative to ref spike 
                timeDiff = spikesRef[s] - targetSpike

                #split on even or odd bins 
                #case 1 - even bin length 
                if numBins % 2 == 0:
                    if timeDiff >= 0 and timeDiff < window_size:
                        binNum = int(midBinRight + np.floor((timeDiff / binsize)))
                    elif timeDiff < 0 and abs(timeDiff) < window_size:
                        binNum = int(midBinLeft - (np.floor(abs(timeDiff) / binsize)))
                #case 2 - odd bin length
                else:
                    #if positive and not middle bin 
                    if timeDiff > binsize :
                        binNum = int(midBin + 1 + np.floor(timeDiff / binsize  ))
                    #negative and not middle bin 
                    elif timeDiff < -1*binsize:
                        binNum = int(midBin - 1 - np.floor(abs(timeDiff) / binsize ))
                    #middle bin - binsize/2 < timeDiff < binsize / 2 
                    else: 
                        binNum = int(midBin)
                self.ACG[binNum] +=1 
        #set the middleBins to be zero(-0.5 ms to +0.5ms bins) 
        if numBins % 2 == 0:
            self.ACG[int(midBinLeft)] = 0
            self.ACG[int(midBinRight)] = 0
        else:
            self.ACG[int(midBin)] = 0
    
    def calc_trough_peak_time(self):
        #trough-peak time is diff(t(global minimum) , t(following local maximum))
        #find the minimum sample 
        minInd = np.argmin(self._waveform)
        maxInd = np.argmax(self._waveform[minInd:])
        #convert samples --> seconds --> milliseconds
        return ((maxInd - minInd) / self.fs) * 1000 
    


    def calc_inst_FR(self):
        return len(self.spike_times) / np.ptp(self.spike_times)
    
    def calc_mean_isi(self, window_size = 50 , binsize = 0.5):
        #get middle bin of ACG
        midBinLeft = int(len(self.ACG) / 2 - 1)
        #take the mean of one side of the ACG 
        leftACG = self.ACG[:midBinLeft - 2]
        t_ccg = np.linspace(start = window_size - (binsize/2), stop = binsize * 3.5 , num = len(leftACG))
        mean_isi = np.sum(leftACG * t_ccg) / np.sum(leftACG)
        return mean_isi


    def calc_ref_violations(self):
    #split on even or odd number of bins 
        if len(self.ACG) % 2 == 0:
            #get midBins(-1.5ms to 1.5ms)
            midBinLeft = int(len(self.ACG) / 2 - 1)
            midBinRight = int(len(self.ACG) / 2)
            #sum from -1.5ms to 1.5ms [midBinLeft - 2 : midBinRight + 3)
            refSpikeCount = sum(self.ACG[int(midBinLeft - 2) : int(midBinRight + 3)])
            fullSpikeCount = sum(self.ACG)
            ref_violations = refSpikeCount / fullSpikeCount * 100
            return ref_violations
        

    def get_unit_type_features(self,ref_violation_thresh = 2):
        from dataAnal.ccg_fit import fit_ACG
        '''features to use for estimating cell type 
            1. trough-peak width(time)
            2. ACG fit coefficient 
            3. Instantaneous firing rate
            4. Mean ISI'''
        unit_features = []
            
        #1. calculate the unit ACG 
        self.calc_unit_ACG(self.spike_times, self.spike_times)
        #2.clean data(mua violations and sparse ACGs(LUA))
        if  max(self.ACG) <= 5:
            self.type = 'lua'
            return
        violations = self.calc_ref_violations()
        if (self.phy_group == 'mua') or (violations > ref_violation_thresh):
            self.type = 'mua'
            return 
        
        ####FEATURE EXTRACTION######
        
        #3 if type not MUA or LUA : 
        #3a - calculate inst FR
        unit_features.append(self.calc_inst_FR())
        #3b - calculate mean ISI
        unit_features.append(self.calc_mean_isi(window_size=50,binsize=.5))
        #3c - calculate the trough to peak time of the unit's best template waveform
        unit_features.append(self.calc_trough_peak_time())
        #3d - fit the exponential model to the ACG
        p_0 = [20, 1, 30, 2, 0.5, 5, 1.5,2]
        lb = [1, 0.1, 0, 0, -30, 0,0.1,0]
        ub = [500, 50, 500, 15, 50, 20,5,100]
        if len(self.ACG) / 2 != 0:
            midBinLeft = len(self.ACG) / 2 - 1
            acg_left = self.ACG[:int(midBinLeft - 2)]
            t_bins = np.linspace(49.75,1.75,num = len(acg_left))
            popt, _ = curve_fit(f = fit_ACG, xdata = acg_left, ydata = t_bins,p0 = p_0,bounds = (lb,ub))
        else:
            '''complete portion later'''
            assert(False)
        
        tau_decay= popt[0]
        tau_rise =  popt[1]
        unit_features.append(tau_decay)
        unit_features.append(tau_rise)

        self.type_features = np.asarray(unit_features)
        
        

        

        




    

    


            
        




        
            

    
