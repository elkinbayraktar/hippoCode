import numpy as np 


def fit_ACG(x,a,b,c,d,e,f,g,h):
    '''a = tau_decay, b = tau_rise, c = decay_amplitude, d = rise_amplitude, e = asymptote, f = refrac, g = tau_burst, h = burst_amplitude'''
    acg_fit = np.max(c * np.exp(-(x - f) / a) - d * np.exp(-(x - f) / b) + h * np.exp(-(x - f) / g) + e, 0)
    return acg_fit
