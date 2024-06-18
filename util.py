from instrument import *
import numpy as np
import pandas as pd

def load_instruments(path='simulations_new.csv'):
    df = pd.read_csv(path, sep=',', header=0)

    # print(df.values)
    instrs = []
    for r in df.values:
        # print(r)
        id = r[0]
        L0 = float(r[1]) * 1e-10
        DL = float(r[2]) * 1e-10 / FWHM_factor
        prec = r[4]
        theta_0 = np.deg2rad(float(r[5]))
        By_min = float(r[6]) * 1e-3
        By_max = float(r[7]) * 1e-3
        instr = Instrument(id, prec, L0, DL, theta_0, By_min, By_max)
        instrs.append(instr)
    return instrs
