import subprocess
import sys
import os

def extract_values(output_filename):
    """Extract various values from the output file."""
    values = {}
    with open(output_filename, 'r') as file:
        lines = file.readlines()
    
    parsing = False
    for line in lines:
        if line.strip() == "-------------------------------------------------":
            parsing = not parsing  # Toggle whether to start or stop parsing
            continue
        
        if parsing:
            parts = line.split()
            key = " ".join(parts[1:-1])  # Join all parts except the first and last to form the key
            value = parts[-1]  # Last part of the split line is the value
            values[key] = value

    return values

def run_xtb(xyz_file, charge, uhf):
    """Run xTB optimization and Hessian calculations for given charge and uhf."""
    base_filename = f"{xyz_file[:-4]}_{charge}_{uhf}"
    output_filename = f"{base_filename}_opt.out"

    method = "--gfn2"

    print(f"Running optimization for charge={charge} and UHF={uhf}...")
    xtb_command = f'xtb {xyz_file} --opt extreme {method}  --chrg {charge} --uhf {uhf} --alpb water  > {output_filename}'
    subprocess.run(xtb_command, shell=True)

    # Move optimized geometry file
    if os.path.exists('xtbopt.xyz'):
        os.rename('xtbopt.xyz', f'{base_filename}.xyz')
    else:
        print("Optimized geometry file not found after xTB optimization.")

    # Run xTB for Hessian calculation with the same charge and spin multiplicity
    output_filename = f"{base_filename}_hess.out"
    print("Calculating Hessian and extracting values...")
#    xtb_command = f'xtb {base_filename}.xyz --gfn2 --chrg {charge} --uhf {uhf} --hess  --solvent h2o > {output_filename}'
    xtb_command = f'xtb {base_filename}.xyz {method} --chrg {charge} --uhf {uhf} --hess  --alpb water  > {output_filename}'
    subprocess.run(xtb_command, shell=True)

    # Extract values from the output file
    values = extract_values(output_filename)
    if values:
        for key, value in values.items():
            print(f"{key}: {value}")
    else:
        print("Values could not be extracted.")

def main(xyz_file):
    # Define combinations of charge and uhf
    combinations = [(3, 6), (2, 5), (0, 5)]

    for charge, uhf in combinations:
        run_xtb(xyz_file, charge, uhf)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python xtb_optimization.py <filename.xyz>")
        sys.exit(1)
    input_xyz = sys.argv[1]
    main(input_xyz)

