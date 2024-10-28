
import os
import shutil
import subprocess

# Directory where xyz files are located
xyz_dir = os.getcwd()
solvation_dir = os.path.join(xyz_dir, "added_solvation")

# Create the added_solvation directory if it doesn't exist
if not os.path.exists(solvation_dir):
    os.mkdir(solvation_dir)

# List of xyz files
xyz_files = [f for f in os.listdir(xyz_dir) if f.endswith(".xyz")]

# Run the hydration shell script for each xyz file and move the output
for xyz_file in xyz_files:
    script_path = "~/Desktop/Codes/solvation_shells/Hydration_shell_radius.py"
    subprocess.run(["python", os.path.expanduser(script_path), xyz_file])
    
    # Assuming the new file has the same name as the original file with some modifications
    generated_xyz = xyz_file.replace(".xyz", "_with_solvation.xyz")  # Modify as per the script's output
    if os.path.exists(generated_xyz):
        shutil.move(generated_xyz, os.path.join(solvation_dir, generated_xyz))
    else:
        print(f"Generated file {generated_xyz} not found")

