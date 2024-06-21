from instrument import *
import numpy as np
import pandas as pd

number_mapping = {
    '1': '2.165',
    '2': '4.321',
    '3': '8', 
    '4': '3',
    '5': '10',
}

letter_mapping = {
    'a': 'FOIL',
    'b': 'WSP',
    'c': 'ISO'
}

def replace_string(input_string):
    # Extract the number and letter from the input string
    number = input_string[0]
    letter = input_string[1]
    
    # Replace the number and letter according to the mappings
    replaced_number = number_mapping.get(number, number)
    replaced_letter = letter_mapping.get(letter, letter)
    
    # Return the concatenated result
    return replaced_letter + ' ' + replaced_number

def load_instruments(path='simulations_new.csv'):
    df = pd.read_csv(path, sep=',', header=0)

    # print(df.values)
    instrs = []
    for r in df.values:
        # print(r)
        id = r[0]
        name = replace_string(id)
        L0 = float(r[1]) * 1e-10
        DL = float(r[2]) * 1e-10 / FWHM_factor
        prec = r[4]
        theta_0 = np.deg2rad(float(r[5]))
        By_min = float(r[6]) * 1e-3
        By_max = float(r[7]) * 1e-3
        instr = Instrument(id, name, prec, L0, DL, theta_0, By_min, By_max)
        instrs.append(instr)
    return instrs
