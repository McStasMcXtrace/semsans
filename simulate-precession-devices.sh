#!/bin/bash
# Script for testing out all precession component variants together to verify that they work as expected
rm -rf data
./full-simulation.sh 1000000 4 5 0,0.005 2.165 0.1 10000 0.001 foil foil_empty GPU; rm -rf foil_data; mv data foil_data
./full-simulation.sh 10000000 4 5 0,0.025 2.165 0.1 10000 0.001 iwsp iwsp_empty GPU; rm -rf iwsp_data; mv data iwsp_data
./full-simulation.sh 10000000 4 5 0,0.025 2.165 0.1 10000 0.001 iso iso_empty GPU; rm -rf iso_data; mv data iso_data