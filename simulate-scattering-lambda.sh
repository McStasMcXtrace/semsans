#!/bin/bash
# Script for simulating scattering for a range of wavelengths
# This is shown on the cover image

# Example usage:
# ./simulate-instr.sh 100000 4 GPU 3000 0.001 1.8 2,12 0.020908 50

# Check if the number of arguments provided is correct
if [ "$#" -ne 9 ]; then
    echo "Usage: $0 <N> <N_threads> <mode> <R> <t> <L_s> <L0_range> <DL> <N_steps>\nmode can be CPU or GPU"
    exit 1
fi

# Assign command-line arguments to variables
N=$1
N_threads=$2
mode=$3
R=$4
t=$5
L_s=$6
L0=$7
DL=$8
N_steps=$9

dir_name="scattering_data"
rm -rf "${dir_name}"
mkdir -p "${dir_name}"

cd instr

if [ $mode == 'CPU' ]; then
    mcrun sample_scattering --mpi=$N_threads -N $N_steps  -n $N L0=$L0 DL=$DL R=$R t=$t L_s=$L_s --dir "../${dir_name}/${R}-${t}"
else
    echo "Running with OpenACC GPU acceleration, this will require the Nvidia HPC toolkit to be installed"
    mcrun sample_scattering --openacc -n $N -N $N_steps L0=$L0 DL=$DL R=$R t=$t L_s=$L_s --dir "../${dir_name}/${R}"
fi