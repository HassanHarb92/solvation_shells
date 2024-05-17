import sys
import math
import numpy as np
from scipy.spatial import ConvexHull

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

def calculate_convex_hull(vertices):
    """
    Calculate the convex hull of a set of points.

    Args:
    vertices (np.ndarray): An array of points.

    Returns:
    ConvexHull: The convex hull of the points.
    """
    hull = ConvexHull(vertices)
    return hull

def place_oxygen_atoms_on_hull(hull, center, radius, n):
    """
    Place oxygen atoms on the convex hull of the molecule.

    Args:
    hull (ConvexHull): The convex hull of the molecule.
    center (tuple): The center (x, y, z) of the molecule.
    radius (float): The radius of the sphere.
    n (int): Number of atoms to place.

    Returns:
    list: A list of tuples representing the (x, y, z) coordinates of each atom.
    """
    vertices = hull.points[hull.vertices]
    atoms = []

    for i in range(n):
        v = vertices[i % len(vertices)]
        direction = v - np.array(center)
        direction /= np.linalg.norm(direction)
        x, y, z = center + radius * direction
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
    angle_rad = math.radians(angle)

    # Initial arbitrary vector for first hydrogen
    v1 = np.array([1, 0, 0])

    # Calculate second vector using cross product to ensure the specified angle
    v2 = np.array([
        math.cos(angle_rad),
        math.sin(angle_rad),
        0
    ])

    # Normalize vectors
    v1 /= np.linalg.norm(v1)
    v2 /= np.linalg.norm(v2)

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
    """
    center = calculate_molecule_center(original_xyz_path)

    with open(original_xyz_path, 'r') as original_file:
        original_lines = original_file.readlines()

    # Extract atom coordinates from the original XYZ file
    atom_coords = []
    for line in original_lines[2:]:
        parts = line.split()
        x, y, z = float(parts[1]), float(parts[2]), float(parts[3])
        atom_coords.append([x, y, z])

    atom_coords = np.array(atom_coords)
    hull = calculate_convex_hull(atom_coords)

    oxygen_atoms = place_oxygen_atoms_on_hull(hull, center, radius, nO)

    with open(new_xyz_path, 'w') as new_file:
        new_file.write(str(int(original_lines[0]) + len(oxygen_atoms) * 3) + '\n')
        new_file.write("Molecule with added oxygen and hydrogen atoms\n")

        for line in original_lines[2:]:
            new_file.write(line)

        for oxygen in oxygen_atoms:
            new_file.write(f"O {oxygen[0]} {oxygen[1]} {oxygen[2]}\n")
            for hydrogen in place_hydrogen_atoms(oxygen, 0.9, 109):
                new_file.write(f"H {hydrogen[0]} {hydrogen[1]} {hydrogen[2]}\n")

def generate_new_file_path(original_path, radius):
    """
    Generate a new file path based on the original path and the radius.

    Args:
    original_path (str): The original file path.
    radius (float): The radius value.

    Returns:
    str: The new file path.
    """
    if original_path.endswith('.xyz'):
        return original_path[:-4] + f"_solvated_radius_{radius}.xyz"
    else:
        return original_path + f"_solvated_radius_{radius}.xyz"

if __name__ == "__main__":
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print("Usage: python script.py <original_xyz_file_path> [radius]")
        sys.exit(1)

    original_xyz_path = sys.argv[1]
    radius = float(sys.argv[2]) if len(sys.argv) == 3 else 5
    new_xyz_path = generate_new_file_path(original_xyz_path, str(int(radius)))
    nO = int(int(radius) * 3)
    print("Number of waters added =", nO)
    create_modified_xyz(original_xyz_path, new_xyz_path, radius, nO)
    print(f"New XYZ file created at {new_xyz_path} with additional oxygen and hydrogen atoms.")

