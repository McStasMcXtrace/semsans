import numpy as np
from scipy.special import j0

def setup_Q_delta_arrays(delta_min, delta_max, Z):
    delta = np.linspace(delta_min, delta_max, Z)
    Q_max = 2 * np.pi / delta_min
    dQ = 0.1 * 2 * np.pi / (Z * (delta_max - delta_min))
    N = int(np.ceil(Q_max / dQ))
    Qn = np.arange(1,N+1) * dQ
    return delta, Qn, dQ, N

def create_hankel_kernels(Qn, dQ, delta, Z):
    j0_Q_delta = j0(np.outer(Qn,delta))
    Q_mat = np.tile(Qn, (Z,1)).transpose()
    H_kernel = Q_mat * j0_Q_delta * dQ
    H_0 = Qn*dQ
    return H_0, H_kernel

def compute_G_matrices(I_Q, H_0, H_kernel, Z):
    G_full =  np.tile(I_Q, (Z,1)).transpose() * H_kernel
    G_full_0 = I_Q * H_0
    return G_full, G_full_0

def compute_total_G_sigma(G_full, G_full_0):
    G_delta_num = np.sum(G_full,axis=0)
    sigma_t_num = np.sum(G_full_0,axis=0)
    return G_delta_num, sigma_t_num

def compute_partial_G_sigma(G_full, G_full_0, sigma_t_num, Z):
    G_partials = np.cumsum(G_full, axis = 0) / sigma_t_num
    sigma_partials = np.cumsum(G_full_0) / sigma_t_num
    G_0_partial = G_partials / np.tile(sigma_partials, (Z,1)).transpose()
    P_partial = np.exp(np.tile(sigma_partials, (Z,1)).transpose() * (G_0_partial - 1))
    return G_partials, sigma_partials, G_0_partial, P_partial