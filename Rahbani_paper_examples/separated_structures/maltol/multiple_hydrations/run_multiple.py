import os
import subprocess
import shutil
import sys

def run_xtb_optimization(input_file, output_file, charge=-1):
    """Run XTB optimization and save the result as the specified output file."""
    command = f"xtb {input_file} --opt --gfn2 --chrg {charge} --alpb water"
    subprocess.run(command, shell=True)
    if os.path.exists("xtbopt.xyz"):
        shutil.move("xtbopt.xyz", output_file)  # Save the optimized file with the desired name

def run_hydration_shell_script(input_file, script_path, output_file):
    """Run the Hydration Shell Radius script to add a water layer and save the result."""
    command = f"python {script_path} {input_file}"
    subprocess.run(command, shell=True)
    if os.path.exists(input_file.replace(".xyz", "_solvated.xyz")):
        shutil.move(input_file.replace(".xyz", "_solvated.xyz"), output_file)  # Rename the generated file

def create_gaussian_input(input_file, charge, multiplicity, title, output_filename):
    """Create Gaussian input file from the specified structure."""
    with open(input_file, "r") as f:
        lines = f.readlines()[2:]  # Skip the first two lines (header and atom count)

    with open(output_filename, "w") as out_f:
        # Writing Gaussian input file
        out_f.write(f"%chk={os.path.splitext(output_filename)[0]}.chk\n")
        out_f.write("#p B3LYP empiricaldispersion=gd3 scrf=(cpcm,solvent=water) scf=(maxcycles=500,xqc,maxconventional=1000) 6-31+G(2df,p)\n\n")
        out_f.write(f"{title}\n\n")
        out_f.write(f"{charge} {multiplicity}\n")
        out_f.writelines(lines)
        out_f.write("\n\n")

def main(input_xyz, script_path):
    # Step 1: Copy the original file for safety
    original_file = "maltonate_original.xyz"
    shutil.copy(input_xyz, original_file)

    # Step 2: XTB Optimization on the original structure
    optimized_file_1 = "maltolate_optimized.xyz"
    run_xtb_optimization(input_xyz, optimized_file_1)

    # Step 3: Add the first solvation layer
    solvated_file_1 = "maltolate_solvated_1.xyz"
    run_hydration_shell_script(optimized_file_1, script_path, solvated_file_1)

    # Step 4: XTB Optimization on the first solvated structure
    optimized_file_2 = "maltolate_solvated_1_optimized.xyz"
    run_xtb_optimization(solvated_file_1, optimized_file_2)

    # Step 5: Add the second solvation layer
    solvated_file_2 = "maltolate_solvated_2.xyz"
    run_hydration_shell_script(optimized_file_2, script_path, solvated_file_2)

    # Step 6: XTB Optimization on the second solvated structure
    optimized_file_3 = "maltolate_solvated_2_optimized.xyz"
    run_xtb_optimization(solvated_file_2, optimized_file_3)

    # Step 7: Add the third solvation layer
    solvated_file_3 = "maltolate_solvated_3.xyz"
    run_hydration_shell_script(optimized_file_3, script_path, solvated_file_3)

    # Step 8: Final XTB Optimization on the third solvated structure
    optimized_file_4 = "maltolate_solvated_3_optimized.xyz"
    run_xtb_optimization(solvated_file_3, optimized_file_4)

    # Step 9: Create Gaussian input files for oxidized and reduced forms
    gaussian_files = [
        {"charge": 0, "multiplicity": 2, "title": "Oxidized Structure", "output": "oxidized.com"},
        {"charge": -1, "multiplicity": 1, "title": "Reduced Structure", "output": "reduced.com"}
    ]

#    for gf in gaussian_files:
#        create_gaussian_input(optimized_file_4, gf["charge"], gf["multiplicity"], gf["title"], gf["output"])

    print("Process completed successfully.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script_name.py <input_xyz_file>")
        sys.exit(1)
    
    input_xyz = sys.argv[1]
    script_path = os.path.expanduser("~/Desktop/Codes/solvation_shells/Hydration_shell_radius.py")

    main(input_xyz, script_path)

