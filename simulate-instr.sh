#!/bin/bash
# Example usage:
# ./simulate-instr.sh 100000 4 0.020908 2.165 0.02 iso.instr GPU

# Check if the number of arguments provided is correct
if [ "$#" -ne 7 ]; then
    echo "Usage: $0 <N> <N_threads> <By> <L0> <DL> <instr> <mode>\nmode can be CPU or GPU"
    exit 1
fi

# Assign command-line arguments to variables
N=$1
N_threads=$2
By=$3
L0=$4
DL=$5
instr=$6
mode=$7

# Generate timestamp
timestamp=$(date +"%Y-%m-%d_%H-%M-%S")

# Rename the directory with timestamp
dir_name="data"
mv "$dir_name" "${dir_name}_${timestamp}"

# Zip the renamed directory
zip -r "${dir_name}_${timestamp}.zip" "${dir_name}_${timestamp}"

# Remove the original directory
# Commenting out this line enables automatic archiving of simulation data
rm -rf "${dir_name}_${timestamp}"
    
mkdir -p data/up
mkdir -p data/down
cd instr

if [ $mode == 'CPU' ]; then
    mcrun $instr --mpi=$N_threads -n $N L0=$L0 DL=$DL By=$By AnaSign=1 --dir "../${dir_name}/up/0"
    mcrun $instr --mpi=$N_threads -n $N L0=$L0 DL=$DL By=$By AnaSign=-1 --dir "../${dir_name}/down/0"
else
    echo "Running with OpenACC GPU acceleration, this will require the Nvidia HPC toolkit to be installed"
    mcrun $instr --openacc -n $N L0=$L0 DL=$DL By=$By AnaSign=1 --dir "../${dir_name}/up/0"
    mcrun $instr --openacc -n $N L0=$L0 DL=$DL By=$By AnaSign=-1 --dir "../${dir_name}/down/0"
fi