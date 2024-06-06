import numpy as np
from scipy.spatial import ConvexHull
import open3d as o3d

# Function to compute the convex hull
def compute_convex_hull(points):
    hull = ConvexHull(points)
    vertices = points[hull.vertices]
    faces = hull.simplices
    return vertices, faces

# Function to smooth the mesh using Laplacian smoothing
def laplacian_smoothing(vertices, faces, iterations=10, lambda_factor=0.5):
    for _ in range(iterations):
        new_vertices = np.copy(vertices)
        for i in range(len(vertices)):
            neighbor_indices = set()
            for face in faces:
                if i in face:
                    neighbor_indices.update(face)
            neighbor_indices.remove(i)
            neighbors = vertices[list(neighbor_indices)]
            new_vertices[i] = vertices[i] + lambda_factor * (np.mean(neighbors, axis=0) - vertices[i])
        vertices = new_vertices
    return vertices

# Function to create Open3D mesh from vertices and faces
def create_mesh(vertices, faces):
    mesh = o3d.geometry.TriangleMesh()
    mesh.vertices = o3d.utility.Vector3dVector(vertices)
    mesh.triangles = o3d.utility.Vector3iVector(faces)
    mesh.compute_vertex_normals()
    return mesh

# Function to sample equidistant points on the mesh surface
def sample_points_on_mesh(mesh, distance):
    pcd = mesh.sample_points_poisson_disk(number_of_points=int(mesh.get_surface_area() / (np.pi * (distance / 2) ** 2)))
    return np.asarray(pcd.points)

# Sample points (replace this with your own points)
points = np.random.rand(30, 3) * 10

# Compute the convex hull
vertices, faces = compute_convex_hull(points)

# Apply Laplacian smoothing
smoothed_vertices = laplacian_smoothing(vertices, faces)

# Create Open3D mesh
mesh = create_mesh(smoothed_vertices, faces)

# Sample equidistant points on the mesh surface
equidistant_points = sample_points_on_mesh(mesh, 4.0)

# Visualize the original mesh and sampled points (optional)
sampled_pcd = o3d.geometry.PointCloud()
sampled_pcd.points = o3d.utility.Vector3dVector(equidistant_points)

o3d.visualization.draw_geometries([mesh, sampled_pcd], window_name='Equidistant Points on Smoothed Convex Hull')

# Output equidistant points to a new .xyz file
with open("equidistant_points.xyz", 'w') as f:
    num_atoms = len(equidistant_points)
    f.write(f"{num_atoms}\n\n")
    for point in equidistant_points:
        f.write(f"O {point[0]} {point[1]} {point[2]}\n")

print("Equidistant points written to equidistant_points.xyz")

