#!/bin/bash
# Example usage:
# ./full-simulation.sh 100000 4 5 0,0.020908 2.165 0.02 10000 0.001 0.095993 1.8 iso iso_empty GPU

# Check if the number of arguments provided is correct
if [ "$#" -ne 13 ]; then
    echo "Usage: $0 <N> <N_threads> <N_steps> <B_min,B_max> <L0> <DL> <R> <t> <theta0_foil> <L_s> <instr_with_sample> <instr_no_sample> <mode>\nmode can be CPU or GPU" 
    exit 1
fi

# Assign command-line arguments to variables
N=$1
N_threads=$2
N_steps=$3
By_range=$4
L0=$5
DL=$6
R=$7
t=$8
theta0_foil=$9
L_s=${10}
instr_with_sample=${11}
instr_no_sample=${12}
mode=${13}

cd instr

if [ $mode == 'CPU' ]; then
    mcrun $instr_with_sample --mpi=$N_threads -n $N -N $N_steps L0=$L0 DL=$DL R=$R t=$t theta0=$theta0_foil L_s=$L_s By=$By_range AnaSign=1
else
    echo "Running with OpenACC GPU acceleration, this will require the CUDA toolkit to be installed"
    mcrun $instr_with_sample --openacc -n $N -N $N_steps L0=$L0 DL=$DL R=$R t=$t theta0=$theta0_foil L_s=$L_s By=$By_range AnaSign=1 
fi