import os
import sys

# Function to extract coordinates from an xyz file
def extract_coordinates(xyz_filename):
    with open(xyz_filename, 'r') as f:
        lines = f.readlines()
    return lines[2:]  # skip first two lines (header and atom count)

# Function to write Gaussian input file
def write_gaussian_input(molecule_name, charge, multiplicity, coordinates, state, spin):
    filename = f"{molecule_name}_{state}_lowspin.com"
    with open(filename, 'w') as f:
        # Write header and route section
        f.write(f"%chk={molecule_name}_{state}_lowspin.chk\n")
        f.write("#p uB3LYP empiricaldispersion=gd3 opt=(cartesian,loose,maxcycles=2000,calcfc) scf=(maxcycles=500,xqc,maxconventional=50) 6-31+G(2df,p)  \n\n")
        f.write(f"{molecule_name} {state} low-spin state\n\n")

        # Write charge and multiplicity
        f.write(f"{charge} {multiplicity}\n")

        # Write coordinates
        f.writelines(coordinates)
        f.write("\n\n")
        f.write("--link1--\n")
        f.write(f"%chk={molecule_name}_{state}_lowspin.chk\n")
        f.write("#p ub3lyp geom=allcheck guess=read chkbasis empiricaldispersion=gd3 scf=(maxcycles=500,xqc,maxconventional=50) scrf=(cpcm,solvent=water)\n\n\n")

# Dictionary containing the charge and multiplicity information
charge_multiplicity = {
    'maltolate': {'red': {'charge': -1, 'low_spin': 1}, 'ox': {'charge': 0, 'low_spin': 2}},
    'deferipronate': {'red': {'charge': -1, 'low_spin': 1}, 'ox': {'charge': 0, 'low_spin': 2}},
    'kojate': {'red': {'charge': -1, 'low_spin': 1}, 'ox': {'charge': 0, 'low_spin': 2}},
    'catecholate': {'red': {'charge': -4, 'low_spin': 1}, 'ox': {'charge': -3, 'low_spin': 2}},
    'salicylate': {'red': {'charge': -4, 'low_spin': 1}, 'ox': {'charge': -3, 'low_spin': 2}}
}

# List of xyz file names
xyz_files = ["catecholate.xyz", "deferipronate.xyz", "kojate.xyz", "salicylate.xyz"]

# Loop through each file and generate Gaussian input files
for xyz_file in xyz_files:
    # Extract the molecule name from the file name (remove .xyz extension)
    molecule_name = os.path.splitext(xyz_file)[0]

    # Extract coordinates from the xyz file
    coordinates = extract_coordinates(xyz_file)

    # Get charge and multiplicity information for the molecule
    if molecule_name in charge_multiplicity:
        for state in ["red", "ox"]:
            charge = charge_multiplicity[molecule_name][state]['charge']
            multiplicity = charge_multiplicity[molecule_name][state]['low_spin']
            write_gaussian_input(molecule_name, charge, multiplicity, coordinates, state, "lowspin")

