import sys
import math
import numpy as np
import os
import subprocess

def calculate_molecule_center(xyz_file_path):
    """
    Calculate the center of a molecule given the path to an xyz file.

    Args:
    xyz_file_path (str): The file path of the xyz file.

    Returns:
    tuple: The (x, y, z) coordinates of the center of the molecule.
    """
    with open(xyz_file_path, 'r') as file:
        lines = file.read().strip().split('\n')
    
    atom_count = int(lines[0])  # The first line indicates the number of atoms

    # Initialize sums for each coordinate
    x_sum, y_sum, z_sum = 0.0, 0.0, 0.0

    for line in lines[2:]:  # Coordinates start from the 3rd line
        parts = line.split()
        x, y, z = float(parts[1]), float(parts[2]), float(parts[3])
        x_sum += x
        y_sum += y
        z_sum += z

    # Calculate the average for each coordinate
    center_x, center_y, center_z = x_sum / atom_count, y_sum / atom_count, z_sum / atom_count

    return (center_x, center_y, center_z)

def calculate_max_distance(center, xyz_file_path):
    """
    Calculate the maximum distance from the center to any atom in the molecule.

    Args:
    center (tuple): The (x, y, z) coordinates of the center of the molecule.
    xyz_file_path (str): The file path of the xyz file.

    Returns:
    float: The maximum distance from the center to any atom.
    """
    with open(xyz_file_path, 'r') as file:
        lines = file.read().strip().split('\n')
    
    max_distance = 0.0

    for line in lines[2:]:  # Coordinates start from the 3rd line
        parts = line.split()
        x, y, z = float(parts[1]), float(parts[2]), float(parts[3])
        distance = math.sqrt((x - center[0])**2 + (y - center[1])**2 + (z - center[2])**2)
        if distance > max_distance:
            max_distance = distance

    return max_distance

def place_oxygen_atoms(center, radius, n):
    """
    Calculate the coordinates of 'n' oxygen atoms placed equidistantly on the surface of a sphere.

    Args:
    center (tuple): The center (x, y, z) of the sphere.
    radius (float): The radius of the sphere.
    n (int): Number of atoms to place.

    Returns:
    list: A list of tuples representing the (x, y, z) coordinates of each atom.
    """
    atoms = []

    # For simplicity, using the vertices of a regular tetrahedron and an additional point
    # This is an approximation and not perfectly equidistant
    for i in range(n):
        # Spherical coordinates
        phi = math.acos(1 - 2 * (i + 0.5) / n)
        theta = math.pi * (1 + 5**0.5) * i

        x = center[0] + radius * math.sin(phi) * math.cos(theta)
        y = center[1] + radius * math.sin(phi) * math.sin(theta)
        z = center[2] + radius * math.cos(phi)

        atoms.append((x, y, z))

    return atoms

def place_hydrogen_atoms(oxygen_atom, oh_distance, angle):
    """
    Calculate the coordinates of two hydrogen atoms for each oxygen atom.

    Args:
    oxygen_atom (tuple): The (x, y, z) coordinates of the oxygen atom.
    oh_distance (float): The O-H distance.
    angle (float): The H-O-H angle in degrees.

    Returns:
    list: A list of tuples representing the (x, y, z) coordinates of each hydrogen atom.
    """
    # Convert angle to radians
    angle_rad = math.radians(angle)

    # Initial arbitrary vector for first hydrogen
    v1 = np.array([1, 0, 0])

    # Calculate second vector using cross product to ensure 109.5 degree angle
    v2 = np.array([
        math.cos(angle_rad),
        math.sqrt(1 - math.cos(angle_rad)**2),
        0
    ])

    # Position the hydrogens relative to the oxygen atom
    h1 = np.array(oxygen_atom) + oh_distance * v1
    h2 = np.array(oxygen_atom) + oh_distance * v2

    return [tuple(h1), tuple(h2)]

def create_modified_xyz(original_xyz_path, new_xyz_path, radius, nO):
    """
    Create a new XYZ file with additional oxygen and hydrogen atoms.

    Args:
    original_xyz_path (str): The file path of the original xyz file.
    new_xyz_path (str): The file path where the new xyz file will be saved.
    radius (float): The radius of the sphere where atoms will be placed.
    nO (int): Number of oxygen atoms to place.

    Returns:
    None
    """
    center = calculate_molecule_center(original_xyz_path)
    oxygen_atoms = place_oxygen_atoms(center, radius, nO)

    with open(original_xyz_path, 'r') as original_file:
        original_lines = original_file.readlines()

    with open(new_xyz_path, 'w') as new_file:
        # Increase the atom count by the number of oxygen atoms and their corresponding hydrogen atoms
        new_file.write(str(int(original_lines[0]) + len(oxygen_atoms) * 3) + '\n')
        new_file.write("Molecule with added oxygen and hydrogen atoms\n")
        # Write the original atoms
        for line in original_lines[2:]:
            new_file.write(line)
        # Append the new oxygen and hydrogen atoms
        new_file.write("\n")
        for oxygen in oxygen_atoms:
            new_file.write(f"O {oxygen[0]} {oxygen[1]} {oxygen[2]}\n")
            for hydrogen in place_hydrogen_atoms(oxygen, 0.9, 109):
                new_file.write(f"H {hydrogen[0]} {hydrogen[1]} {hydrogen[2]}\n")

def generate_new_file_path(original_path):
    """
    Generate a new file path based on the original path.

    Args:
    original_path (str): The original file path.

    Returns:
    str: The new file path.
    """
    if original_path.endswith('.xyz'):
        return original_path[:-4] + "_solvated.xyz"
    else:
        return original_path + "_solvated.xyz"

def run_xtb_and_move(new_xyz_path, original_xyz_path):
    """
    Run xtb optimization and move the optimized file to a new folder.

    Args:
    new_xyz_path (str): The file path of the new xyz file.
    original_xyz_path (str): The original xyz file path to derive the new filename.

    Returns:
    None
    """
    # Run xtb optimization
    subprocess.run(['xtb', new_xyz_path, '--opt', '--gfn2', '--chrg', '1', '--uhf', '1', '--alpb', 'water'], check=True)

    # Define new file names and paths
    optimized_file = 'xtbopt.xyz'
    new_optimized_file = new_xyz_path.replace('_solvated.xyz', '_solvated_opt.xyz')
    new_folder = 'xyz_xtb_opt'

    # Create the new folder if it doesn't exist
    os.makedirs(new_folder, exist_ok=True)

    # Move the optimized file to the new folder with the new name
    os.rename(optimized_file, os.path.join(new_folder, os.path.basename(new_optimized_file)))

# Main program
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <original_xyz_file_path>")
        sys.exit(1)

    original_xyz_path = sys.argv[1]
    center = calculate_molecule_center(original_xyz_path)
    max_distance = calculate_max_distance(center, original_xyz_path)
    radius = max_distance + 1.5
    new_xyz_path = generate_new_file_path(original_xyz_path)
    nO = int(radius * 3)
    print("Number of waters added =", nO)
    create_modified_xyz(original_xyz_path, new_xyz_path, radius, nO)
    print(f"New XYZ file created at {new_xyz_path} with additional oxygen and hydrogen atoms.")
    
    run_xtb_and_move(new_xyz_path, original_xyz_path)
    print(f"Optimization completed and file moved to 'xyz_xtb_opt' folder.")

