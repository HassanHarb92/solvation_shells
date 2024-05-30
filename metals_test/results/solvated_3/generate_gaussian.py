import os

# Define functionals and metals information
functionals = {
    "B3LYP": "B3LYP empiricaldispersion=gd3",
#    "BLYP": "BLYP empiricaldispersion=gd3",
#    "HSE06": "HSEH1PBE",
#    "M08-HX": "M08HX",
#    "svwn": "svwn",
#    "PBE0": "PBE1PBE empiricaldispersion=gd3"
}

metals_info = {
    "Ti": [(2, 3), (3, 2)],
    "V": [(2, 4), (3, 3)],
    "Cr": [(2, 5), (3, 4)],
    "Mn": [(2, 6), (3, 5)]
}

# Directory containing the .xyz files
xyz_directory = "."
# Directory to save the .com files
com_directory = "." #"../com_files_solvated"
os.makedirs(com_directory, exist_ok=True)

# Function to read .xyz file content
def read_xyz_file(filepath):
    with open(filepath, 'r') as file:
        lines = file.readlines()
    # Remove first two lines and join the rest as a single string
    return ''.join(lines[2:])

# Function to create .com file content
def create_com_content(metal, charge, functional, xyz_content):
    func_name = functionals[functional]
#    dispersion = " empiricaldispersion=gd3" if "empiricaldispersion=gd3" in func_name else ""
    multiplicity = next((m for (c, m) in metals_info[metal] if c == int(charge)), 1)
    
    com_content = f"""%chk={metal}_{charge}_{functional}
#p {func_name} 6-31+G(2df,p) scf=(maxcycles=500,xqc,maxconventional=50) scrf=(cpcm,solvent=water)

title

{charge}  {multiplicity}
{xyz_content}


"""
    return com_content

# Iterate over all .xyz files and generate .com files
for xyz_filename in os.listdir(xyz_directory):
    if xyz_filename.endswith(".xyz"):
        parts = xyz_filename.split('_')
        metal, charge, functional = parts[0], parts[1], parts[2]
        
        xyz_filepath = os.path.join(xyz_directory, xyz_filename)
        xyz_content = read_xyz_file(xyz_filepath)
        
        com_content = create_com_content(metal, charge, functional, xyz_content)
        com_filename = f"{metal}_{charge}_{functional}.com"
        com_filepath = os.path.join(com_directory, com_filename)
        
        with open(com_filepath, 'w') as com_file:
            com_file.write(com_content)

print("Gaussian input files (.com) have been generated successfully.")

