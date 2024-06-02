import numpy as np
import re

# Sample volume thickness
t = 0.001 # m
# Radius of sphere, equal to 1 um but expressed in AA
R = 10000e-10 # m
# Volume ratio
phi = 0.015
delta_rho = 6e10 * (1e2) ** 2 # 1/m^2 (?)

c = 4.63e14 # T-1 m-2
theta_0 = np.deg2rad(5.5) # rad
wavelength = 2.165e-10 # m


def s_t(R = R, t = t, wavelength = wavelength, phi=phi, delta_rho=delta_rho):
    return 3/2 * phi * (1 - phi) * delta_rho**2 * wavelength**2 * t * R


def compute_p_0(By, wavelength, theta_0):
    delta_B = By
    p_0 = np.pi * np.tan(theta_0) / (c * wavelength * delta_B)
    return p_0

# Computes the z corresponding to a certain By given other fixed parameters
def compute_z(By, theta_0 = theta_0, wavelength=wavelength, L_s = 1.8):
    # B_2 - B_1 generally
    delta_B = By
    # Distance from detector to sample
    z = c * wavelength ** 2 * delta_B * L_s / (np.pi * np.tan(theta_0))
    return z

# Computes By given z and other fixed parameters
def compute_By(z):
    # Distance from detector to sample
    L_s = 1.8 # m
    delta_B = np.pi * np.tan(theta_0) * z / (c * wavelength ** 2 * L_s)
    return delta_B


def G_0(xi):
    res = np.zeros_like(xi)
    res[xi>=2.0] = 0
    valid_xi = xi[xi<2.0]
    res[xi<2.0] = np.sqrt(1 - (valid_xi / 2) ** 2) * (1 + valid_xi ** 2 / 8)\
         + 1 / 2 * valid_xi ** 2 * (1 - (valid_xi / 4 ) ** 2) * np.log(valid_xi / (2 + np.sqrt(4 - valid_xi ** 2)))
    return res

def G(z, R):
    xi = z/R
    return s_t(R) * G_0(xi)

def G_norm(z, R):
    xi = z/R
    return G_0(xi)

def compute_P_dark_field(I_up,I_down):
    return  (I_up - I_down) / (I_up + I_down)

# Data processing helper functions
def extract_By(file):
    with open(file) as f:
        text = f.read()
        
        match = re.search(r'# Param: By=([0-9.]+)', text)
        assert(match)
        return float(match.group(1))
    
def get_data(i, folder='data'):
    y, I_up = np.genfromtxt(f'{folder}/up/{i}/det.dat', delimiter=' ', usecols=(0,1), unpack=True)
    _, I_down = np.genfromtxt(f'{folder}/down/{i}/det.dat', delimiter=' ', usecols=(0,1), unpack=True)
    _, I_empty_up = np.genfromtxt(f'{folder}/empty_up/{i}/det.dat', delimiter=' ', usecols=(0,1), unpack=True)
    _, I_empty_down = np.genfromtxt(f'{folder}/empty_down/{i}/det.dat', delimiter=' ', usecols=(0,1), unpack=True)
    By = extract_By(f'{folder}/up/{i}/det.dat')
    return y, I_up, I_down, I_empty_up, I_empty_down, By

def indices_within_range(x, a, b):
    return np.where((x >= a) & (x <= b))[0]