def generate_gaussian_input(xyz_file, checkpoint_name, charge, multiplicity, title, method, basis_set, output_file):
    with open(xyz_file, 'r') as f:
        xyz_data = f.readlines()[2:]  # Skip the first two lines of XYZ format

    gaussian_input = f"""%chk={checkpoint_name}
#p {method} {basis_set} empiricaldispersion=gd3 scf=(maxcycles=500,xqc,maxconventional=50) opt=(cartesian,RecalcFC=10,MaxCycles=10000) freq=raman

{title}

{charge} {multiplicity}
{''.join(xyz_data)}

"""

    with open(output_file, 'w') as f:
        f.write(gaussian_input)
        print(f"Gaussian input file '{output_file}' generated successfully.")

# Define parameters
xyz_file = 'fe_boric_acid.xyz'
checkpoint_name = 'fe_boric_acid'
title = 'Fe Boric Acid Complex'
method = 'uB3LYP'
basis_set = '6-31+G(2df,p)'

# Charge and multiplicity combinations
combinations = [(2, 5), (2, 1), (3, 6), (3, 2)]

# Generate Gaussian input files for each combination
for charge, multiplicity in combinations:
    output_file = f"fe_boric_acid_{charge}_{multiplicity}.com"
    generate_gaussian_input(xyz_file, checkpoint_name, charge, multiplicity, title, method, basis_set, output_file)
