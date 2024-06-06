import sys
import numpy as np
from scipy.spatial import ConvexHull
from scipy.spatial.distance import cdist

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

def generate_points_on_expanded_hull(hull, centroid, expansion_distance, point_spacing):
    expanded_vertices = []
    for vertex in hull.points[hull.vertices]:
        direction = vertex - centroid
        norm_direction = direction / np.linalg.norm(direction)
        expanded_vertex = vertex + expansion_distance * norm_direction
        expanded_vertices.append(expanded_vertex)

    expanded_vertices = np.array(expanded_vertices)

    # Sample points on the surface of the expanded convex hull
    hull_expanded = ConvexHull(expanded_vertices)
    sampled_points = []
    for simplex in hull_expanded.simplices:
        simplex_points = expanded_vertices[simplex]
        for i, p1 in enumerate(simplex_points):
            for j in range(i+1, len(simplex_points)):
                p2 = simplex_points[j]
                vec = p2 - p1
                dist = np.linalg.norm(vec)
                num_samples = int(dist // point_spacing)
                for k in range(1, num_samples):
                    sampled_points.append(p1 + (k * point_spacing / dist) * vec)

    sampled_points = np.array(sampled_points)
    # Remove points that are too close to each other
    if len(sampled_points) > 0:
        dist_matrix = cdist(sampled_points, sampled_points)
        np.fill_diagonal(dist_matrix, np.inf)
        mask = np.all(dist_matrix >= point_spacing, axis=0)
        sampled_points = sampled_points[mask]
    return sampled_points

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <file.xyz>")
        sys.exit(1)

    filename = sys.argv[1]
    atom_types, points = read_xyz(filename)

    # Calculate the convex hull
    hull = ConvexHull(points)

    # Calculate the centroid of the hull
    centroid = np.mean(points[hull.vertices], axis=0)

    # Generate points on the surface of the expanded convex hull
    expansion_distance = 2.0
    point_spacing = 3.0
    O_atoms = generate_points_on_expanded_hull(hull, centroid, expansion_distance, point_spacing)

    # Place hydrogen atoms
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

