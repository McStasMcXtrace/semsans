#!/bin/bash
# Example usage:
# ./full-simulation.sh 100000 4 5 0,0.020908 2.165 0.02 10000 0.001 iso iso_empty GPU

# Check if the number of arguments provided is correct
if [ "$#" -ne 11 ]; then
    echo "Usage: $0 <N> <N_threads> <N_steps> <B_min,B_max> <L0> <DL> <R> <t> <instr_with_sample> <instr_no_sample> <mode>\nmode can be CPU or GPU" 
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
instr_with_sample=$9
instr_no_sample=${10}
mode=${11}

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
    mcrun $instr_with_sample --mpi=$N_threads -n $N -N $N_steps L0=$L0 DL=$DL R=$R t=$t By=$By_range AnaSign=1 --dir "../${dir_name}/up" 
    mcrun $instr_with_sample --mpi=$N_threads -n $N -N $N_steps L0=$L0 DL=$DL R=$R t=$t By=$By_range AnaSign=-1 --dir "../${dir_name}/down"
    mcrun $instr_no_sample --mpi=$N_threads -n $N -N $N_steps L0=$L0 DL=$DL R=$R t=$t By=$By_range AnaSign=1 --dir "../${dir_name}/empty_up"
    mcrun $instr_no_sample --mpi=$N_threads -n $N -N $N_steps L0=$L0 DL=$DL R=$R t=$t By=$By_range AnaSign=-1 --dir "../${dir_name}/empty_down"
else
    echo "Running with OpenACC GPU acceleration, this will require the CUDA toolkit to be installed"
    mcrun $instr_with_sample --openacc -n $N -N $N_steps L0=$L0 DL=$DL R=$R t=$t By=$By_range AnaSign=1 --dir "../${dir_name}/up" 
    mcrun $instr_with_sample --openacc -n $N -N $N_steps L0=$L0 DL=$DL R=$R t=$t By=$By_range AnaSign=-1 --dir "../${dir_name}/down"
    mcrun $instr_no_sample --openacc -n $N -N $N_steps L0=$L0 DL=$DL R=$R t=$t By=$By_range AnaSign=1 --dir "../${dir_name}/empty_up"
    mcrun $instr_no_sample --openacc -n $N -N $N_steps L0=$L0 DL=$DL R=$R t=$t By=$By_range AnaSign=-1 --dir "../${dir_name}/empty_down"
fi