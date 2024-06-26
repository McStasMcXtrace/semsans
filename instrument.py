import numpy as np
from definitions import *
FWHM_env_min = 2e-3

class Instrument:
    def __init__(self, id: str, name: str, prec_type: str, L0: float, DL: float, theta_0: float, By_min: float, By_max: float, L_s: float = 1.8, L_1: float = 4, L_2: float = 2, detector_size = detector_size):
        self.id = id
        self.name = name
        self.prec_type = prec_type
        self.L0 = L0
        self.DL = DL
        self.theta_0 = theta_0
        self.detector_size = detector_size
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
        f_min = 1/self.detector_size
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
    
    def delta_range_var_L_s(self):
        L_s_min, L_s_max = self.L_s_min(), self.L_s_max()
        d_min, d_max = self.delta_min(), self.delta_max()
        return L_s_min / self.L_s * d_min, L_s_max / self.L_s * d_max
    
    def Q_max(self):
        return np.pi / self.delta_min_detector()

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
    
    def theta_a(self):
        return np.arctan(self.detector_size / (2 * self.L_s))
    
    def L_s_min(self, theta_a_max = 15e-3):
        return self.detector_size / (2 * np.tan(theta_a_max))
    
    def L_s_max(self, d_p = 0.3, t_max = 0.01):
        return self.L_2 - d_p / 2 - t_max/2
    
    def L_s_range(self):
        return self.L_s_min(), self.L_s_max()
            
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
        Q_max = self.Q_max()
        theta_a = self.theta_a() * 1e3
        R_max = 1 / (Q_max * 1e-10)
        L_s_min, L_s_max = self.L_s_range()
        delta_min_var, delta_max_var = self.delta_range_var_L_s()
        return f"""Instrument ID {self.id}; Name: {self.name}
    \tSource: L0 = {self.L0 * 1e10} Å; sigma_L = {self.DL * 1e10} Å
    \tPrecession device: {self.prec_type_long()}; theta_0 = {round(self.theta_0,2)} rad; By_min = {self.By_min * 1e3}mT; By_max = {self.By_max * 1e3}mT
    \tL_1 = {round(self.L_1, 2)}m; L_2 = {round(self.L_2, 2)}m;  L_s = {round(self.L_s, 2)}m
    \tδ range from precession devices: {round(delta_min_field * 1e9,1)} - {round(d_max_field * 1e9, 1)}nm
    \tmin δ for 1 period on detector with height {detector_size * 1e3}mm: {round(d_min * 1e9,1)}nm 
    \tmax δ for sampling at 10s/period (f_0 = {round(f_s / 10 *1e-3)}mm^-1): {round(delta_max_ten_samples * 1e9,1)}nm
    \tmax δ for envelope FWHM due to wavelength spread >= {FWHM_env_min*1e3}mm: {round(delta_max_env * 1e9,1)}nm
    \tQ_max as determined by detector height and distance: {round(Q_max * 1e-10, 7)} Å-1
    \tApproximate max R of solid sphere sample: {round(R_max * 0.1, 2)} - {round(R_max,2)} nm
    \ttheta_a: {round(theta_a, 2)} mrad
    \tL_s range: {round(L_s_min, 2)} - {round(L_s_max, 2)} m
    \tfinal δ range: {round(d_min * 1e9,1)} - {round(d_max * 1e9, 1)}nm ({min_name} - {max_name} limited)
    \tfinal δ range with variable L_s: {round(delta_min_var * 1e9,1)} - {round(delta_max_var * 1e9, 1)}nm"""
    
def print_latex_tables(instrs):
    for i in [0,1]:
        for instr in instrs[3:-6]:
            print(instr)
            delta_max_field = instr.delta_max_B_field()
            delta_max_env = instr.delta_max_envelope()
            delta_max_ten_samples = instr.delta_max_sampling()
            # print(F"Max delta ideal sampling (10 samples per period) (f_0 = {round(f_ten_samples*1e-3)}mm^-1: {round(delta_max_ten_samples * 1e9,2)}nm")
            maxes = [(delta_max_ten_samples, 'sampling'), (delta_max_env, 'envelope'), (delta_max_field, 'precession devices') ]
            (delta_max, max_name) = min(maxes)
            delta_min_field = instr.delta_min_B_field()
            delta_min_single_period = instr.delta_min_detector()
            mins = [(delta_min_single_period, 'detector size'), (delta_min_field, 'precession devices')]
            (delta_min, min_name) = max(mins)
            # print(min_max)
            Q_max = instr.Q_max()
            # print(f"{a}")
            r = lambda x: round(x * 1e9,2)
            if i==0:
                print(f"{instr.name} & {r(delta_min_single_period)} & {r(delta_min_field)} & {r(delta_max_ten_samples)} & {r(delta_max_env)} & {r(delta_max_field)} \\\\")
            else:
                print(f"{instr.name} & {round(Q_max * 1e-10, 5)} & {r(delta_min)} & {r(delta_max)} \\\\")
if __name__ == '__main__':
    import util
    instrs = util.load_instruments('instruments.csv')
    print_latex_tables(instrs)