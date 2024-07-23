#!/bin/bash

# Loop over all .xyz files in the current directory
for xyz_file in *.xyz; do
    # Define the namespace prefix (you can customize this as needed)
    namespace_prefix="${xyz_file%.xyz}_namespace"
    
    # Run the xtb command
    xtb "$xyz_file" --opt --gfn2 --chrg 2 --cmaes --maxstep 0.2 200 --cycles 1000 --gfniter 3000 --namespace "$namespace_prefix"
    
    # Check if the command was successful
    if [ $? -eq 0 ]; then
        echo "Successfully processed $xyz_file"
    else
        echo "Error processing $xyz_file"
    fi
done

