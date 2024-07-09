import os

# Dictionary with charge and multiplicity information
charge_multiplicity = {
    'Cr_2_B3LYP': {'charge': 2, 'multiplicity': 5},
    'Cr_3_B3LYP': {'charge': 3, 'multiplicity': 4},
    'Mn_2_B3LYP': {'charge': 2, 'multiplicity': 6},
    'Mn_3_B3LYP': {'charge': 3, 'multiplicity': 5},
    'Ti_2_B3LYP': {'charge': 2, 'multiplicity': 3},
    'Ti_3_B3LYP': {'charge': 3, 'multiplicity': 2},
    'V_2_B3LYP': {'charge': 2, 'multiplicity': 4},
    'V_3_B3LYP': {'charge': 3, 'multiplicity': 3}
}

# List of basis sets with labels
basis_sets = {
    'B1': '6-31+G(2df,p)',
    'B2': '6-31++G(2df,p)',
    'B3': 'aug-cc-pvtz',
    'B4': 'cc-pvtz',
    'B5': 'def2TZVP',
    'B6': 'CEP-31G',
    'B7': '3-21G',
    'B8': '6-311G(3df,3pd)',
    'B9': '6-311+G(3df,3pd)',
    'B10': '6-311++G(3df,3pd)'
}

def read_xyz_file(xyz_filepath):
    with open(xyz_filepath, 'r') as file:
        lines = file.readlines()[2:]  # Skip the first two lines
    return ''.join(lines)

def generate_gaussian_input(metal, charge, multiplicity, basis_label, basis_set, xyz_content):
    filename = f"{metal}_{charge}_{basis_label}.com"
    content = f"""%chk={metal}_{charge}_{basis_label}.chk
#p B3LYP empiricaldispersion=gd3 {basis_set} scf=(maxcycles=500,xqc,maxconventional=500) scrf=(cpcm,solvent=water)

title

{charge} {multiplicity}
{xyz_content}



"""
    with open(filename, 'w') as file:
        file.write(content)

def main():
    xyz_files = [file for file in os.listdir() if file.endswith('.xyz')]
    
    for xyz_file in xyz_files:
        # Extract the metal and charge info from the filename
        metal_charge_label = xyz_file.replace('.xyz', '')
        
        if metal_charge_label in charge_multiplicity:
            charge = charge_multiplicity[metal_charge_label]['charge']
            multiplicity = charge_multiplicity[metal_charge_label]['multiplicity']
            xyz_content = read_xyz_file(xyz_file)
            
            for basis_label, basis_set in basis_sets.items():
                generate_gaussian_input(metal_charge_label, charge, multiplicity, basis_label, basis_set, xyz_content)

if __name__ == "__main__":
    main()

