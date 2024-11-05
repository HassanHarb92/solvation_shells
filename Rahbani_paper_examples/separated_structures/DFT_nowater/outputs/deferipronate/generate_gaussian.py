import os
import glob

# Define the Gaussian job parameters for oxidized and reduced forms
gaussian_files = [
    {"charge": 0, "multiplicity": 2, "title": "Oxidized_Structure"},
    {"charge": -1, "multiplicity": 1, "title": "Reduced_Structure"}
]

def create_gaussian_input(xyz_filename, charge, multiplicity, title):
    # Read the coordinates from the .xyz file
    with open(xyz_filename, 'r') as f:
        lines = f.readlines()
    # Skip the first two lines (number of atoms and comment)
    coord_lines = lines[2:]

    # Create the output filename
    base_name = os.path.splitext(xyz_filename)[0]
    output_filename = f"{base_name}_{title}.com"

    # Write the Gaussian input file
    with open(output_filename, "w") as out_f:
        # Writing Gaussian input file
        out_f.write(f"%chk={base_name}_{title}.chk\n")
        out_f.write("#p B3LYP empiricaldispersion=gd3 scrf=(cpcm,solvent=water) "
                    "scf=(maxcycles=500,xqc,maxconventional=1000) 6-31+G(2df,p)\n\n")
        out_f.write(f"{title}\n\n")
        out_f.write(f"{charge} {multiplicity}\n")
        out_f.writelines(coord_lines)
        out_f.write("\n\n")

    print(f"Generated Gaussian input file: {output_filename}")

def main():
    # Get a list of all .xyz files in the current directory
    xyz_files = glob.glob("*.xyz")
    if not xyz_files:
        print("No .xyz files found in the current directory.")
        return

    for xyz_file in xyz_files:
        for params in gaussian_files:
            create_gaussian_input(
                xyz_filename=xyz_file,
                charge=params["charge"],
                multiplicity=params["multiplicity"],
                title=params["title"]
            )

if __name__ == "__main__":
    main()

