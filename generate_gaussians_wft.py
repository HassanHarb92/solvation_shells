import os

functionals = {
    "mp2": "mp2=full",
    "mp3": "mp3=full",
    "mp4": "mp4=full",
    
    "cis": "cis=full",
    "cid": "cid=full",
    "cisd": "cisd=full",

    "ccs": "ccs=full",
    "ccd": "ccd=full",
    "ccsd": "ccsd=full"
    # New functionals added here
}



directories = ["fe_6H2O", "fe_18H2O"]

for directory in directories:
    for filename in os.listdir(directory):
        if filename.endswith(".xyz"):
            # Extract charge and multiplicity from the filename
            parts = filename[:-4].split('_')
            charge = parts[-2]
            multiplicity = parts[-1]
            
            for func_key, func_name in functionals.items():
                # Check for dispersion
                dispersion = " " #" empiricaldispersion=gd3" if func_key in functionals_with_dispersion else ""
                
                # Create the Gaussian input file name
                output_filename = f"{parts[0]}_{parts[1]}_{func_key}_{charge}_{multiplicity}.com"
                output_path = os.path.join(directory, output_filename)
                
                # Read the XYZ coordinates from the file
                with open(os.path.join(directory, filename), 'r') as file:
                    lines = file.readlines()
                
                # Write the Gaussian input file
                with open(output_path, 'w') as outfile:
                    outfile.write(f"%chk={output_filename[:-4]}.chk\n")
                    outfile.write(f"#p {func_name} 6-31+G(2df,p){dispersion} scf=(maxcycles=500,xqc,maxconventional=50) scrf=(cpcm,solvent=water)\n\n")
                    outfile.write(f"{filename[:-4]}\n\n")
                    outfile.write(f"{charge} {multiplicity}\n")
                    outfile.writelines(lines[2:])  # Skip the first two lines of the XYZ file
                    outfile.write("\n\n\n")



