import sys
import numpy as np
from scipy.spatial import ConvexHull
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

def read_xyz(file):
    with open(file, 'r') as f:
        lines = f.readlines()
        num_atoms = int(lines[0])
        coordinates = []
        for line in lines[2:2 + num_atoms]:
            parts = line.split()
            coordinates.append([float(parts[1]), float(parts[2]), float(parts[3])])
    return np.array(coordinates)

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
    points = read_xyz(filename)

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
        num_atoms = len(O_atoms) + len(H_atoms)
        f.write(f"{num_atoms}\n\n")
        for O in O_atoms:
            f.write(f"O {O[0]} {O[1]} {O[2]}\n")
        for H in H_atoms:
            f.write(f"H {H[0]} {H[1]} {H[2]}\n")

    # Visualization
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Plot the original points
    ax.scatter(points[:, 0], points[:, 1], points[:, 2], color='b')

    # Plot the original convex hull
    for simplex in hull.simplices:
        ax.plot(points[simplex, 0], points[simplex, 1], points[simplex, 2], 'k-')

    # Plot the expanded convex hull
    ax.scatter(expanded_vertices[:, 0], expanded_vertices[:, 1], expanded_vertices[:, 2], color='r')

    for simplex in hull.simplices:
        ax.plot(expanded_vertices[simplex, 0], expanded_vertices[simplex, 1], expanded_vertices[simplex, 2], 'r--')

    # Plot O atoms
    ax.scatter(O_atoms[:, 0], O_atoms[:, 1], O_atoms[:, 2], color='orange', label='O')

    # Plot H atoms
    H_atoms = np.array(H_atoms)
    ax.scatter(H_atoms[:, 0], H_atoms[:, 1], H_atoms[:, 2], color='green', label='H')

    ax.add_collection3d(Poly3DCollection(expanded_vertices[hull.simplices], facecolors='cyan', linewidths=1, edgecolors='r', alpha=.25))

    plt.legend()
    plt.show()

