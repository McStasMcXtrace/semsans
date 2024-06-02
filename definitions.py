import numpy as np
import re

# Factor for converting a sigma to a FWHM and back
FWHM_factor = 2 * np.sqrt(2 * np.log(2))

detector_pixel_size = 10e-6 # m

# Detector sampling rate
f_s = 1/detector_pixel_size

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
L_s = 1.8 # m


def s_t(R = R, t = t, wavelength = wavelength, phi=phi, delta_rho=delta_rho):
    return 3/2 * phi * (1 - phi) * delta_rho**2 * wavelength**2 * t * R


def compute_p_0(By, wavelength, theta_0):
    delta_B = By
    p_0 = np.pi * np.tan(theta_0) / (c * wavelength * delta_B)
    return p_0

# Computes the z corresponding to a certain By given other fixed parameters
def compute_z(By, theta_0 = theta_0, wavelength=wavelength, L_s = L_s):
    # B_2 - B_1 generally
    delta_B = By
    # Distance from detector to sample
    z = c * wavelength ** 2 * delta_B * L_s / (np.pi * np.tan(theta_0))
    return z

# Computes By given z and other fixed parameters
def compute_By(z, L_s = L_s):
    # Distance from detector to sample
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
def extract_parameters(file):
    parameters = {}
    pattern = re.compile(r'# Param:\s*(\w+)=([\d\.]+)')
    with open(file, 'r') as file:
        for line in file:
            match = pattern.search(line)
            if match:
                param_name = match.group(1)
                param_value = float(match.group(2))
                parameters[param_name] = param_value
    return parameters

def get_data(i, folder='data'):
    y, I_up = np.genfromtxt(f'{folder}/up/{i}/det.dat', delimiter=' ', usecols=(0,1), unpack=True)
    _, I_down = np.genfromtxt(f'{folder}/down/{i}/det.dat', delimiter=' ', usecols=(0,1), unpack=True)
    _, I_empty_up = np.genfromtxt(f'{folder}/empty_up/{i}/det.dat', delimiter=' ', usecols=(0,1), unpack=True)
    _, I_empty_down = np.genfromtxt(f'{folder}/empty_down/{i}/det.dat', delimiter=' ', usecols=(0,1), unpack=True)
    parameters = extract_parameters(f'{folder}/up/{i}/det.dat')
    By = parameters['By']
    return y, I_up, I_down, I_empty_up, I_empty_down, By

def indices_within_range(x, a, b):
    return np.where((x >= a) & (x <= b))[0]