import os
import shutil
import subprocess

# Directory where xyz files are located
xyz_dir = os.getcwd()
solvation_dir = os.path.join(xyz_dir, "added_solvation")

# Create the added_solvation directory if it doesn't exist
if not os.path.exists(solvation_dir):
    os.mkdir(solvation_dir)

# List of xyz files that contain "low_spin" in their name
xyz_files = [f for f in os.listdir(xyz_dir) if f.endswith(".xyz") and "_red_" in f]

# Run the hydration shell script for each low_spin xyz file and move the output
for xyz_file in xyz_files:
    print("Processing file:", xyz_file)
    script_path = "~/Desktop/Codes/solvation_shells/Hydration_shell_radius.py"
    
    try:
        # Run the hydration shell script
        subprocess.run(["python", os.path.expanduser(script_path), xyz_file])

        # Modify the expected output file to match the correct suffix
        generated_xyz = xyz_file.replace(".xyz", "_solvated.xyz")  # Now matching _solvated suffix
        if os.path.exists(generated_xyz):
            # Move the generated low_spin file to the solvation directory
            shutil.move(generated_xyz, os.path.join(solvation_dir, generated_xyz))

            # Create an ox version of the file by copying and renaming it
            ox_xyz = generated_xyz.replace("_red_", "_ox_")
            shutil.copy(os.path.join(solvation_dir, generated_xyz), os.path.join(solvation_dir, ox_xyz))
            print(f"Generated ox file: {ox_xyz}")
        else:
            print(f"Generated file {generated_xyz} not found")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while processing {xyz_file}: {e}")

