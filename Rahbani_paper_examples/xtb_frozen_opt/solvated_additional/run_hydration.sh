#!/bin/bash

# Loop through all .xyz files in the current directory
for file in *.xyz; do
    echo "Processing $file ..."
    # Run the Python script on each .xyz file
    python ~/Desktop/Codes/solvation_shells/Hydration_shell_radius.py "$file"
done

