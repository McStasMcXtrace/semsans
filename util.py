from instrument import *
import numpy as np
import pandas as pd

def find_overlap(interval1, interval2):
    a1, a2 = interval1
    b1, b2 = interval2

    # Calculate the start and end of the overlap interval
    start = max(a1, b1)
    end = min(a2, b2)

    # Check if there is an actual overlap
    if start <= end:
        return (start, end)
    else:
        return None  # No overlap

def overlap_percentage(interval1, interval2):
    b1, b2 = interval2
    overlap = find_overlap(interval1, interval2)
    if overlap == None:
        return 0
    else:
        (c1, c2) = overlap
        # Overlap as fraction of interval 2 (b)
        fraction = (c2 - c1) / (b2 - b1) * 100
        return fraction 
    
def log_overlap_percentage(interval1, interval2):
    return overlap_percentage(np.log(interval1), np.log(interval2))

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
