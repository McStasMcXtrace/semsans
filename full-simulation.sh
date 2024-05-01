#!/bin/bash
# Check if the number of arguments provided is correct
if [ "$#" -ne 4 ]; then
    echo "Usage: $0 <N> <N_steps> <N_threads> <B_min,B_max>"
    exit 1
fi

# Assign command-line arguments to variables
N=$1
N_threads=$2
N_steps=$3
By_range=$4

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
mcrun base.instr --mpi=$N_threads -n $N -N $N_steps L0=2.165 DL=0.02 By=$By_range AnaSign=1 --dir data/base_up
mcrun base.instr --mpi=$N_threads -n $N -N $N_steps L0=2.165 DL=0.02 By=$By_range AnaSign=-1 --dir data/base_down
mcrun base_no_sample.instr --mpi=$N_threads -n $N -N $N_steps L0=2.165 DL=0.02 By=$By_range AnaSign=1 --dir data/base_no_sample_up
mcrun base_no_sample.instr --mpi=$N_threads -n $N -N $N_steps L0=2.165 DL=0.02 By=0,0.020908 AnaSign=-1 --dir data/base_no_sample_down