import os
import shutil
import subprocess
import sys

def create_frozen_input(filename, frozen_count):
    """Create a frozen atoms input file for XTB."""
    with open("salicylate_frozen.inp", "w") as f:
        f.write("$fix\n")
        f.write(f"  atoms: 1-{frozen_count}\n")
        f.write("$end\n")

def run_xtb_optimization(input_file, output_file, charge=-4, frozen_input="salicylate_frozen.inp"):
    """Run XTB optimization with frozen atoms."""
    command = f"xtb {input_file} --opt --gfn2 --chrg {charge} --alpb water --input {frozen_input}"
    subprocess.run(command, shell=True)
    if os.path.exists("xtbopt.xyz"):
        shutil.move("xtbopt.xyz", output_file)

def run_hydration_shell_script(input_file, script_path, output_file):
    """Run the Hydration Shell Radius script to add a water layer."""
    command = f"python {script_path} {input_file}"
    subprocess.run(command, shell=True)
    solvated_file = input_file.replace(".xyz", "_solvated.xyz")
    if os.path.exists(solvated_file):
        shutil.move(solvated_file, output_file)

def main(input_xyz, script_path):
    # Step 1: Read the number of atoms to freeze
    with open(input_xyz, "r") as f:
        num_atoms = int(f.readline().strip())

    # Step 2: Create the frozen input file for XTB
    create_frozen_input(input_xyz, num_atoms)

    # Step 3: Copy the original file for reference
    shutil.copy(input_xyz, "salicylate_original.xyz")
    shutil.copy(input_xyz, "salicylate_optimized.xyz")
    # Step 4: XTB Optimization on the original structure
    optimized_file_1 = "salicylate_optimized.xyz"
#    run_xtb_optimization(input_xyz, optimized_file_1)

    # Step 5: Add the first solvation shell
    solvated_file_1 = "salicylate_solvated_1.xyz"
    run_hydration_shell_script(optimized_file_1, script_path, solvated_file_1)

    # Step 6: XTB Optimization on the first solvated structure
    optimized_file_2 = "salicylate_solvated_1_optimized.xyz"
    run_xtb_optimization(solvated_file_1, optimized_file_2)

    # Step 7: Add the second solvation shell
    solvated_file_2 = "salicylate_solvated_2.xyz"
    run_hydration_shell_script(optimized_file_2, script_path, solvated_file_2)

    # Step 8: XTB Optimization on the second solvated structure
    optimized_file_3 = "salicylate_solvated_2_optimized.xyz"
    run_xtb_optimization(solvated_file_2, optimized_file_3)

    # Step 9: Add the third solvation shell
    solvated_file_3 = "salicylate_solvated_3.xyz"
    run_hydration_shell_script(optimized_file_3, script_path, solvated_file_3)

    # Step 10: Final XTB Optimization on the third solvated structure
    optimized_file_4 = "salicylate_solvated_3_optimized.xyz"
    run_xtb_optimization(solvated_file_3, optimized_file_4)

    print("Process completed successfully.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script_name.py <input_xyz_file>")
        sys.exit(1)
    
    input_xyz = sys.argv[1]
    script_path = os.path.expanduser("~/Desktop/Codes/solvation_shells/Hydration_shell_radius.py")

    main(input_xyz, script_path)

