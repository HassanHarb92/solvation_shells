import os

# Function to extract coordinates from an xyz file
def extract_coordinates(xyz_filename):
    with open(xyz_filename, 'r') as f:
        lines = f.readlines()
    return lines[2:]  # skip first two lines (header and atom count)

# Function to write Gaussian input file
def write_gaussian_input(molecule_name, charge, multiplicity, coordinates, state, spin):
    filename = f"{molecule_name}_{state}_{spin}.com"
    with open(filename, 'w') as f:
        # Write header and route section
        f.write(f"%chk={molecule_name}_{state}_{spin}.chk\n")
        f.write("#p B3LYP empiricaldispersion=gd3 scrf=(cpcm,solvent=water) scf=(maxcycles=500,xqc,maxconventional=50) 6-31+G(2df,p)  \n\n")
        f.write(f"{molecule_name} {state} {spin} spin\n\n")
        
        # Write charge and multiplicity
        f.write(f"{charge} {multiplicity}\n")
        
        # Write coordinates
        f.writelines(coordinates)
        f.write("\n\n")

# Dictionary containing the charge and multiplicity information
charge_multiplicity = {
    'maltolate': {'red': {'charge': -1, 'low_spin': 1, 'high_spin': 5}, 'ox': {'charge': 0, 'low_spin': 2, 'high_spin': 6}},
    'deferipronate': {'red': {'charge': -1, 'low_spin': 1, 'high_spin': 5}, 'ox': {'charge': 0, 'low_spin': 2, 'high_spin': 6}},
    'kojate': {'red': {'charge': -1, 'low_spin': 1, 'high_spin': 5}, 'ox': {'charge': 0, 'low_spin': 2, 'high_spin': 6}},
    'catecholate': {'red': {'charge': -4, 'low_spin': 1, 'high_spin': 5}, 'ox': {'charge': -3, 'low_spin': 2, 'high_spin': 6}},
    'salicylate': {'red': {'charge': -4, 'low_spin': 1, 'high_spin': 5}, 'ox': {'charge': -3, 'low_spin': 2, 'high_spin': 6}}
}

# Directory where solvation xyz files are stored
solvation_dir = "./added_solvation"
solvated_xyz_files = [f for f in os.listdir(solvation_dir) if f.endswith(".xyz")]

# Generate Gaussian input files for each solvation xyz file
for solvated_xyz in solvated_xyz_files:
    molecule_name, state, spin = solvated_xyz.split('_')[:3]
    spin = 'low_spin' if 'low' in spin else 'high_spin'
    
    # Extract charge and multiplicity
    charge = charge_multiplicity[molecule_name][state]['charge']
    multiplicity = charge_multiplicity[molecule_name][state][spin]
    
    # Extract coordinates and write Gaussian input file
    coordinates = extract_coordinates(os.path.join(solvation_dir, solvated_xyz))
    write_gaussian_input(molecule_name, charge, multiplicity, coordinates, state, spin)

