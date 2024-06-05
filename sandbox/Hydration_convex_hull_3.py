import sys
import numpy as np
from scipy.spatial import ConvexHull, Delaunay

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

def generate_points_on_convex_hull(points, distance=5.0):
    # Calculate the convex hull
    hull = ConvexHull(points)
    hull_points = points[hull.vertices]

    # Calculate the centroid of the hull
    centroid = np.mean(hull_points, axis=0)

    # Create a new set of expanded vertices
    expanded_vertices = []
    for vertex in hull_points:
        direction = vertex - centroid
        norm_direction = direction / np.linalg.norm(direction)
        expanded_vertex = vertex + 2 * norm_direction
        expanded_vertices.append(expanded_vertex)

    expanded_vertices = np.array(expanded_vertices)
    
    # Sample points on the surface of the expanded convex hull
    delaunay = Delaunay(expanded_vertices)
    simplex_points = expanded_vertices[delaunay.simplices]
    
    surface_points = []
    for simplex in simplex_points:
        for i in range(3):
            start = simplex[i]
            end = simplex[(i + 1) % 3]
            vec = end - start
            norm_vec = vec / np.linalg.norm(vec)
            num_segments = int(np.linalg.norm(vec) // distance)
            for j in range(num_segments):
                surface_points.append(start + j * distance * norm_vec)
                
    return np.array(surface_points)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <file.xyz>")
        sys.exit(1)

    filename = sys.argv[1]
    atom_types, points = read_xyz(filename)

    # Generate points on the surface of the expanded convex hull
    O_atoms = generate_points_on_convex_hull(points)

    # Place hydrogen atoms
    H_atoms = []
    for O in O_atoms:
        direction = O - np.mean(O_atoms, axis=0)
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

