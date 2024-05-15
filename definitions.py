import numpy as np

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

s_t = 3/2 * phi * (1 - phi) * delta_rho**2 * wavelength**2 * t * R

def compute_p_0(By):
    delta_B = By
    p_0 = np.pi * np.tan(theta_0) / (c * wavelength * delta_B)
    return p_0

# Computes the z corresponding to a certain By given other fixed parameters
def compute_z(By):
    # B_2 - B_1 generally
    delta_B = By
    # Distance between centers of the 2 flippers
    L = 2 # m
    z = c * wavelength ** 2 * delta_B * L / (np.pi * np.tan(theta_0))
    return z

# Computes By given z and other fixed parameters
def compute_By(z):
    # Distance between centers of the 2 flippers
    L = 2 # m
    delta_B = np.pi * np.tan(theta_0) * z / (c * wavelength ** 2 * L)
    return delta_B


def G_0(xi):
    res = np.zeros_like(xi)
    res[xi>=2.0] = 0
    valid_xi = xi[xi<2.0]
    res[xi<2.0] = np.sqrt(1 - (valid_xi / 2) ** 2) * (1 + valid_xi ** 2 / 8)\
         + 1 / 2 * valid_xi ** 2 * (1 - (valid_xi / 4 ) ** 2) * np.log(valid_xi / (2 + np.sqrt(4 - valid_xi ** 2)))
    return res

def G(xi):
    return s_t * G_0(xi)

def compute_P_dark_field(I_up,I_down):
    return  (I_up - I_down) / (I_up + I_down)

def get_data(i):
    y, I_up = np.genfromtxt(f'data/up/{i}/det.dat', delimiter=' ', usecols=(0,1), unpack=True)
    _, I_down = np.genfromtxt(f'data/down/{i}/det.dat', delimiter=' ', usecols=(0,1), unpack=True)
    _, I_empty_up = np.genfromtxt(f'data/no_sample_up/{i}/det.dat', delimiter=' ', usecols=(0,1), unpack=True)
    _, I_empty_down = np.genfromtxt(f'data/no_sample_down/{i}/det.dat', delimiter=' ', usecols=(0,1), unpack=True)
    return y, I_up, I_down, I_empty_up, I_empty_down