import sys
import numpy as np
from scipy.spatial import ConvexHull
import open3d as o3d

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

def compute_convex_hull(points):
    hull = ConvexHull(points)
    vertices = points[hull.vertices]
    faces = hull.simplices
    return vertices, faces, hull.vertices

def laplacian_smoothing(vertices, faces, iterations=50, lambda_factor=0.5):
    # Create an adjacency list
    adjacency_list = {i: set() for i in range(len(vertices))}
    for face in faces:
        for i, j in zip(face, np.roll(face, -1)):
            adjacency_list[i].add(j)
            adjacency_list[j].add(i)
    
    for _ in range(iterations):
        new_vertices = np.copy(vertices)
        for i in range(len(vertices)):
            neighbors = np.array([vertices[j] for j in adjacency_list[i]])
            new_vertices[i] = vertices[i] + lambda_factor * (np.mean(neighbors, axis=0) - vertices[i])
        vertices = new_vertices
    return vertices

def create_mesh(vertices, faces):
    mesh = o3d.geometry.TriangleMesh()
    mesh.vertices = o3d.utility.Vector3dVector(vertices)
    mesh.triangles = o3d.utility.Vector3iVector(faces)
    mesh.compute_vertex_normals()
    return mesh

def sample_points_on_mesh(mesh, num_points):
    pcd = mesh.sample_points_uniformly(number_of_points=num_points)
    return np.asarray(pcd.points)

def generate_and_filter_points(mesh, points, num_points_to_sample, min_distance):
    sampled_points = sample_points_on_mesh(mesh, num_points_to_sample)
    filtered_points = []
    for point in sampled_points:
        if np.all(np.linalg.norm(points - point, axis=1) >= min_distance):
            filtered_points.append(point)
    return np.array(filtered_points)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <file.xyz>")
        sys.exit(1)

    filename = sys.argv[1]
    atom_types, points = read_xyz(filename)

    # Calculate the convex hull
    vertices, faces, vertex_indices = compute_convex_hull(points)

    # Map faces to vertex indices
    mapped_faces = np.array([[np.where(vertex_indices == idx)[0][0] for idx in face] for face in faces])

    # Expand convex hull vertices by 2 units
    centroid = np.mean(vertices, axis=0)
    expanded_vertices = []
    for vertex in vertices:
        direction = vertex - centroid
        norm_direction = direction / np.linalg.norm(direction)
        expanded_vertex = vertex + 2 * norm_direction
        expanded_vertices.append(expanded_vertex)

    expanded_vertices = np.array(expanded_vertices)

    # Apply Laplacian smoothing with increased iterations
    smoothed_vertices = laplacian_smoothing(expanded_vertices, mapped_faces, iterations=100, lambda_factor=0.4)

    # Create Open3D mesh
    mesh = create_mesh(smoothed_vertices, mapped_faces)

    # Generate and filter points on the mesh surface
    num_points_to_sample = 10000  # Start with a large number of points
    min_distance = 4.0
    filtered_O_atoms = generate_and_filter_points(mesh, points, num_points_to_sample, min_distance)

    while len(filtered_O_atoms) == 0:
        print(f"No suitable points found with {num_points_to_sample} samples. Increasing sample size.")
        num_points_to_sample *= 2
        filtered_O_atoms = generate_and_filter_points(mesh, points, num_points_to_sample, min_distance)

    # Place hydrogen atoms
    H_atoms = []
    for O in filtered_O_atoms:
        direction = O - centroid
        H1, H2 = place_hydrogens(O, direction)
        H_atoms.append(H1)
        H_atoms.append(H2)

    # Output the results to a new .xyz file
    with open("expanded_structure_with_smooth_hull.xyz", 'w') as f:
        num_atoms = len(points) + len(filtered_O_atoms) + len(H_atoms)
        f.write(f"{num_atoms}\n\n")
        
        # Write original atoms
        for atom_type, point in zip(atom_types, points):
            f.write(f"{atom_type} {point[0]} {point[1]} {point[2]}\n")
        
        # Write expanded O atoms
        for O in filtered_O_atoms:
            f.write(f"O {O[0]} {O[1]} {O[2]}\n")
        
        # Write H atoms
        for H in H_atoms:
            f.write(f"H {H[0]} {H[1]} {H[2]}\n")

    print("Expanded structure with smooth hull written to expanded_structure_with_smooth_hull.xyz")

