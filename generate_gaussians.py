
import os

functionals = {
    "B3LYP": "B3LYP", "PBE0": "PBE1PBE", "BLYP": "BLYP", "PBE": "PBEPBE",
    "M06": "M06", "M06-2X": "M062X", "M06-L": "M06L", "M06-HF": "M06HF",
    "CAM-B3LYP": "CAM-B3LYP", "wB97X-D": "wB97XD", "wB97X": "wB97X", "wB97": "wB97",
    "HSE06": "HSEH1PBE", "TPSSh": "TPSSH", "B3PW91": "B3PW91", "B97D": "B97D",
    "X3LYP": "X3LYP", "B2PLYP": "B2PLYP", "MPW1PW91": "MPW1PW91",
    "OLYP": "OLYP", "OPBE": "OPBE", "OTPSS": "OTPSS", "O3LYP": "O3LYP",
    "BMK": "BMK", "M05": "M05", "M05-2X": "M052X", "M08-HX": "M08HX", "UHF": "UHF",
#    "mp2=full": "mp2=full",
#    "ccsd=full": "ccsd=full",
    # New functionals added here
    "SPW91": "SPW91", "svwn": "svwn", "bpw91": "bpw91", "n12": "n12", "OVWN5": "OVWN5"
}


functionals_with_dispersion = ["B2PLYPD3", "B97D3", "B3LYP", "BLYP", "PBE1PBE",
                               "TPSSTPSS", "PBEPBE", "BP86", "BPBE", "B3PW91",
                               "BMK", "CAM–B3LYP", "LC-wPBE", "M05", "M052X",
                               "M06L", "M06", "M062X", "M06HF", "PW6B95D3" ,'UHF']

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
                dispersion = " empiricaldispersion=gd3" if func_key in functionals_with_dispersion else ""
                
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



