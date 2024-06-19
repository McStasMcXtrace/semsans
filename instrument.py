import numpy as np
from definitions import *
FWHM_env_min = 1e-3
# L_s_reduction = 0.75
# For simulating variable L_s
# L_s_min = 1.5 
class Instrument:
    def __init__(self, id: str,  prec_type: str, L0: float, DL: float, theta_0: float, By_min: float, By_max: float, L_s: float = 1.8, L_1: float = 4, L_2: float = 2):
        self.id = id
        self.prec_type = prec_type
        self.L0 = L0
        self.DL = DL
        self.theta_0 = theta_0
        self.By_min = By_min 
        self.By_max = By_max
        self.L_s = L_s
        self.L_1 = L_1
        self.L_2 = L_2

    # Minimum reachable delta as follows from B field. 
    def delta_min_B_field(self):
        return compute_z(self.By_min * abs(1 - self.L_1 / self.L_2),self.theta_0,self.L0,self.L_s)
    
    # Limit to have at least 1 modulation period on the detector
    def delta_min_detector(self):
        f_min = 1/detector_size
        delta_min_sampling = f_min * self.L0 * self.L_s
        return delta_min_sampling

    def delta_min_named(self):
        delta_min_field = self.delta_min_B_field()
        delta_min_single_period = self.delta_min_detector()
        mins = [(delta_min_field, 'B strength'), (delta_min_single_period, 'detector size')]
        (d_min, min_name) = max(mins)
        return (d_min, min_name)
    
    def delta_min(self):
        return self.delta_min_named()[0]

    def delta_max_named(self):
        d_max_field = self.delta_max_B_field()
        delta_max_env = self.delta_max_envelope()
        delta_max_ten_samples = self.delta_max_sampling()
        maxes = [(d_max_field, 'B strength'), (delta_max_env, 'envelope'), (delta_max_ten_samples, 'sampling')]
        (d_max, max_name) = min(maxes)
        return (d_max, max_name) 

    def delta_max(self):
        return self.delta_max_named()[0]
    
    def delta_max_B_field(self):
        # Due to the focussing condition, one component will have field By_max/2 and the other By_max, giving a delta of By_max/2
        return compute_z(self.By_max * (1 - self.L_2 / self.L_1), self.theta_0, self.L0, self.L_s)

    def delta_max_sampling(self, samples = 5):
        f_s = 1/detector_pixel_size
        f_super_sampled = f_s / samples
        delta_max_sampling = f_super_sampled * self.L0 * self.L_s
        return delta_max_sampling

    def delta_max_envelope(self):
        delta_max_env = np.sqrt(2 * np.log(2)) * self.L0**2 * self.L_s / (np.pi * self.DL * FWHM_env_min)
        return delta_max_env
    
    def delta_range_B_field(self):
        return self.delta_min_B_field(), self.delta_max_B_field()
    
    def delta_range(self):
        return self.delta_min(), self.delta_max()

    def prec_type_long(self):
        long_str = ''
        match self.prec_type:
            case 'iso':  
                long_str = 'isosceles triangle'
            case 'wsp':
                long_str = 'Wollaston prism'
            case 'foil':
                long_str = 'foil flipper'
        return long_str

            
    def __str__(self):
        d_max_field = self.delta_max_B_field()
        delta_max_env = self.delta_max_envelope()
        delta_max_ten_samples = self.delta_max_sampling()
        # print(F"Max delta ideal sampling (10 samples per period) (f_0 = {round(f_ten_samples*1e-3)}mm^-1: {round(delta_max_ten_samples * 1e9,2)}nm")
        maxes = [(d_max_field, 'precession devices'), (delta_max_env, 'envelope'), (delta_max_ten_samples, 'sampling')]
        (d_max, max_name) = min(maxes)
        delta_min_field = self.delta_min_B_field()
        delta_min_single_period = self.delta_min_detector()
        mins = [(delta_min_field, 'precession devices'), (delta_min_single_period, 'detector size')]
        (d_min, min_name) = max(mins)
        # print(min_max)
        return f"""Instrument ID {self.id}
    \tSource: L0 = {self.L0 * 1e10} Å; sigma_L = {self.DL * 1e10} Å
    \tPrecession device: {self.prec_type_long()}; theta_0 = {round(self.theta_0,2)} rad; By_min = {self.By_min * 1e3}mT; By_max = {self.By_max * 1e3}mT
    \tL_1 = {round(self.L_1, 2)}m; L_2 = {round(self.L_2, 2)}m;  L_s = {round(self.L_s, 2)}m
    \tδ range from precession devices: {round(delta_min_field * 1e9,1)} - {round(d_max_field * 1e9, 1)}nm
    \tmin δ for 1 period on detector with height {detector_size * 1e3}mm: {round(d_min * 1e9,1)}nm 
    \tmax δ for sampling at 10s/period (f_0 = {round(f_s / 10 *1e-3)}mm^-1): {round(delta_max_ten_samples * 1e9,1)}nm
    \tmax δ for envelope FWHM due to wavelength spread >= {FWHM_env_min*1e3}mm: {round(delta_max_env * 1e9,1)}nm
    \tfinal δ range: {round(d_min * 1e9,1)} - {round(d_max * 1e9, 1)}nm ({min_name} - {max_name} limited)"""
    