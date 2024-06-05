import sys
import numpy as np
from scipy.spatial import ConvexHull

def read_xyz(file):
    with open(file, 'r') as f:
        lines = f.readlines()
        num_atoms = int(lines[0])
        atom_types = []
        coordinates = []
        for line in lines[2:2 + num_atoms]:
            parts = line.split()
            atom_types.append(parts[0])
            coordinates.append([float(parts[1]), float(parts[2]), float(parts[3])])
    return atom_types, np.array(coordinates)

def place_hydrogens(O, direction):
    angle = 109.5 * np.pi / 180  # Convert angle to radians
    distance = 0.95

    # Compute orthogonal vectors
    norm_direction = direction / np.linalg.norm(direction)
    not_collinear = np.array([1, 0, 0]) if abs(norm_direction[0]) < abs(norm_direction[1]) else np.array([0, 1, 0])
    perpendicular = np.cross(norm_direction, not_collinear)
    perpendicular /= np.linalg.norm(perpendicular)

    # Rotation vectors
    H1 = O + distance * (np.cos(angle / 2) * norm_direction + np.sin(angle / 2) * perpendicular)
    H2 = O + distance * (np.cos(angle / 2) * norm_direction - np.sin(angle / 2) * perpendicular)

    return H1, H2

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <file.xyz>")
        sys.exit(1)

    filename = sys.argv[1]
    atom_types, points = read_xyz(filename)

    # Calculate the convex hull
    hull = ConvexHull(points)
    hull_vertices = points[hull.vertices]

    # Calculate the centroid of the hull
    centroid = np.mean(hull_vertices, axis=0)

    # Create a new set of expanded vertices
    expanded_vertices = []
    for vertex in hull_vertices:
        direction = vertex - centroid
        norm_direction = direction / np.linalg.norm(direction)
        expanded_vertex = vertex + 2 * norm_direction
        expanded_vertices.append(expanded_vertex)

    expanded_vertices = np.array(expanded_vertices)

    # Place O and H atoms
    O_atoms = expanded_vertices
    H_atoms = []
    for O in O_atoms:
        direction = O - centroid
        H1, H2 = place_hydrogens(O, direction)
        H_atoms.append(H1)
        H_atoms.append(H2)

    # Output the results to a new .xyz file
    with open("expanded_structure.xyz", 'w') as f:
        num_atoms = len(points) + len(O_atoms) + len(H_atoms)
        f.write(f"{num_atoms}\n\n")
        
        # Write original atoms
        for atom_type, point in zip(atom_types, points):
            f.write(f"{atom_type} {point[0]} {point[1]} {point[2]}\n")
        
        # Write expanded O atoms
        for O in O_atoms:
            f.write(f"O {O[0]} {O[1]} {O[2]}\n")
        
        # Write H atoms
        for H in H_atoms:
            f.write(f"H {H[0]} {H[1]} {H[2]}\n")

    print("Expanded structure written to expanded_structure.xyz")

