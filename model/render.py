import trimesh
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection, Line3DCollection
import os
import numpy as np

# Load your model
path = '/sdcard/math/model.glb'
loaded = trimesh.load(path)

# Output folder
output_dir = '/sdcard/math/frames/'
os.makedirs(output_dir, exist_ok=True)

# Set up figure
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.axis('off')

# Function to plot 3D paths (if any)
def plot_path3d(path_obj):
    for entity in path_obj.entities:
        points = path_obj.vertices[entity.points]
        ax.add_collection3d(Line3DCollection([points], colors='cyan', linewidths=1.5))
    return path_obj.vertices

# Function to plot a mesh without outlines or blue
def plot_mesh(mesh_obj):
    vertices = mesh_obj.vertices
    faces = mesh_obj.faces

    mesh = Poly3DCollection(
        vertices[faces],
        facecolors=(1, 1, 1, 1),   # Solid white
        edgecolors='none',        # Force no edges
        linewidths=0,             # No line width
        antialiased=False         # Prevent anti-alias glow
    )
    ax.add_collection3d(mesh)
    return vertices

# Helper: extract individual meshes from Scene/list/single
def extract_all_geometries(obj):
    if isinstance(obj, trimesh.Scene):
        return list(obj.dump())
    elif isinstance(obj, list):
        return obj
    else:
        return [obj]

geometries = extract_all_geometries(loaded)

# Render frames
for i, angle in enumerate(range(0, 360, 5)):
    ax.cla()
    ax.axis('off')
    all_vertices = []

    for geo in geometries:
        if isinstance(geo, trimesh.Trimesh):
            v = plot_mesh(geo)
        elif isinstance(geo, trimesh.path.path.Path3D):
            v = plot_path3d(geo)
        else:
            continue
        all_vertices.append(v)

    if all_vertices:
        combined = np.vstack(all_vertices)
        scale = combined.flatten()
        ax.auto_scale_xyz(scale, scale, scale)

    ax.view_init(elev=30, azim=angle)

    frame_path = os.path.join(output_dir, f'frame_{i:03d}.png')
    plt.savefig(frame_path, dpi=200, transparent=True, bbox_inches='tight', pad_inches=0)

plt.close(fig)
