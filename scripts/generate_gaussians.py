import os

# Define the directory containing the .xyz files
#xyz_directory = "/lcrc/project/Cat_Biomass/Hassan/C-steel/Fe_Boryls/Fe_boryls_xyz/xyz_xtb_opt"
xyz_directory = "/lcrc/project/Cat_Biomass/Hassan/C-steel/Fe_Boryls/Fe_boryls_xyz/second_solvation_shell/xyz_files"
# Define charge and multiplicity
charge = 2
multiplicity = 2

# List all .xyz files in the directory
xyz_files = [f for f in os.listdir(xyz_directory) if f.endswith('.xyz')]

# Template for the Gaussian input file
gaussian_template = """%chk={chk_name}
#p uB3LYP 6-31+G(2df,p) empiricaldispersion=gd3 scf=(maxcycles=500,xqc,maxconventional=500) scrf=(cpcm,solvent=water)

{title}

{charge} {multiplicity}
{coordinates}

"""

# Generate Gaussian input files
for xyz_file in xyz_files:
    file_base = os.path.splitext(xyz_file)[0]
    com_file = file_base + ".com"
    chk_name = file_base + ".chk"
    title = file_base

    # Read the coordinates from the .xyz file
    with open(os.path.join(xyz_directory, xyz_file), 'r') as f:
        lines = f.readlines()[2:]  # Skip the first two lines (atom count and comment)
        coordinates = ''.join(lines).strip()

    # Create the content of the Gaussian input file
    gaussian_input = gaussian_template.format(
        chk_name=chk_name,
        title=title,
        charge=charge,
        multiplicity=multiplicity,
        coordinates=coordinates
    )

    # Write the Gaussian input file
    with open(os.path.join(xyz_directory, com_file), 'w') as f:
        f.write(gaussian_input)

print(f"Generated Gaussian input files for {len(xyz_files)} .xyz files in {xyz_directory}")

