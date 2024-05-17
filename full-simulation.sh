#!/bin/bash
# Example usage for 1e5 neutrons on 4 threads with 5 By field steps from 0 to 0.020908 T (corresponding to z from 0 to 3 um for base.instr)
# ./full-simulation.sh 100000 4 5 0,0.020908 foil.instr foil_empty.instr

# Check if the number of arguments provided is correct
if [ "$#" -ne 7 ]; then
    echo "Usage: $0 <N> <N_threads> <N_steps> <B_min,B_max> <instr_with_sample> <instr_no_sample> <mode>\nmode can be CPU or GPU" 
    exit 1
fi

# Assign command-line arguments to variables
N=$1
N_threads=$2
N_steps=$3
By_range=$4
instr_with_sample=$5
instr_no_sample=$6
mode=$7

# Generate timestamp
timestamp=$(date +"%Y-%m-%d_%H-%M-%S")

# Rename the directory with timestamp
dir_name="data"
mv "$dir_name" "${dir_name}_${timestamp}"

# Zip the renamed directory
zip -r "${dir_name}_${timestamp}.zip" "${dir_name}_${timestamp}"

# Remove the original directory
rm -rf "${dir_name}_${timestamp}"
    
mkdir data
cd instr

if [ $mode == 'CPU' ]; then
    mcrun $instr_with_sample --mpi=$N_threads -n $N -N $N_steps L0=2.165 DL=0.02 By=$By_range AnaSign=1 --dir "../${dir_name}/up" 
    mcrun $instr_with_sample --mpi=$N_threads -n $N -N $N_steps L0=2.165 DL=0.02 By=$By_range AnaSign=-1 --dir "../${dir_name}/down"
    mcrun $instr_no_sample --mpi=$N_threads -n $N -N $N_steps L0=2.165 DL=0.02 By=$By_range AnaSign=1 --dir "../${dir_name}/empty_up"
    mcrun $instr_no_sample --mpi=$N_threads -n $N -N $N_steps L0=2.165 DL=0.02 By=$By_range AnaSign=-1 --dir "../${dir_name}/empty_down"
else
    echo "Running with OpenACC GPU acceleration, this will require the CUDA toolkit to be installed"
    mcrun $instr_with_sample --openacc -n $N -N $N_steps L0=2.165 DL=0.02 By=$By_range AnaSign=1 --dir "../${dir_name}/up" 
    mcrun $instr_with_sample --openacc -n $N -N $N_steps L0=2.165 DL=0.02 By=$By_range AnaSign=-1 --dir "../${dir_name}/down"
    mcrun $instr_no_sample --openacc -n $N -N $N_steps L0=2.165 DL=0.02 By=$By_range AnaSign=1 --dir "../${dir_name}/empty_up"
    mcrun $instr_no_sample --openacc -n $N -N $N_steps L0=2.165 DL=0.02 By=$By_range AnaSign=-1 --dir "../${dir_name}/empty_down"
fi