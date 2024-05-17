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

def enlarge_hull_vertices(hull, center, additional_distance):
    """
    Enlarge the convex hull by increasing the distance of each vertex from the center.

    Args:
    hull (ConvexHull): The convex hull of the molecule.
    center (tuple): The center (x, y, z) of the molecule.
    additional_distance (float): The distance by which to enlarge the hull.

    Returns:
    np.ndarray: The enlarged vertices of the convex hull.
    """
    enlarged_vertices = []
    for vertex in hull.points[hull.vertices]:
        direction = vertex - np.array(center)
        direction /= np.linalg.norm(direction)
        enlarged_vertex = np.array(center) + (np.linalg.norm(vertex - np.array(center)) + additional_distance) * direction
        enlarged_vertices.append(enlarged_vertex)
    return np.array(enlarged_vertices)

def fibonacci_sphere(samples, radius):
    """
    Generate points on the surface of a sphere using the Fibonacci lattice method.

    Args:
    samples (int): Number of points to generate.
    radius (float): Radius of the sphere.

    Returns:
    list: A list of tuples representing the (x, y, z) coordinates of each point.
    """
    points = []
    phi = math.pi * (3.0 - math.sqrt(5.0))  # golden angle in radians

    for i in range(samples):
        y = 1 - (i / float(samples - 1)) * 2  # y goes from 1 to -1
        radius_at_y = math.sqrt(1 - y * y)  # radius at y

        theta = phi * i  # golden angle increment

        x = math.cos(theta) * radius_at_y
        z = math.sin(theta) * radius_at_y

        points.append((x * radius, y * radius, z * radius))

    return points

def map_to_hull(points, hull, center, additional_distance):
    """
    Map points generated on a sphere to the enlarged convex hull.

    Args:
    points (list): Points on the surface of a sphere.
    hull (ConvexHull): The convex hull of the molecule.
    center (tuple): The center (x, y, z) of the molecule.
    additional_distance (float): The distance by which to enlarge the hull.

    Returns:
    list: A list of tuples representing the (x, y, z) coordinates of each point on the hull.
    """
    hull_vertices = hull.points[hull.vertices]
    mapped_points = []

    for point in points:
        direction = point - np.array(center)
        direction /= np.linalg.norm(direction)
        mapped_point = np.array(center) + (np.linalg.norm(hull_vertices[0] - np.array(center)) + additional_distance) * direction
        mapped_points.append(mapped_point)

    return mapped_points

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

    # Initial arbitrary vector for first hydrogen (as a float array)
    v1 = np.array([1.0, 0.0, 0.0])

    # Calculate second vector using the angle
    v2 = np.array([
        math.cos(angle_rad),
        math.sin(angle_rad),
        0.0
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

    enlarged_vertices = enlarge_hull_vertices(hull, center, 2.0)
    sphere_points = fibonacci_sphere(nO, radius)
    oxygen_atoms = map_to_hull(sphere_points, hull, center, 2.0)

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

