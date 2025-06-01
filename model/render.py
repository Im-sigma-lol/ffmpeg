import trimesh
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection, Line3DCollection
import os
import numpy as np

# Path to your GLB file — using /sdcard for Termux compatibility
path = '/sdcard/math/model.glb'
loaded = trimesh.load(path)

# Output directory for rendered frames
output_dir = '/sdcard/math/frames/'
os.makedirs(output_dir, exist_ok=True)

# Create a 3D figure
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.axis('off')

# Function to plot 3D line paths (if present)
def plot_path3d(path_obj):
    for entity in path_obj.entities:
        points = path_obj.vertices[entity.points]
        ax.add_collection3d(Line3DCollection([points], colors='cyan', linewidths=1.5))
    return path_obj.vertices

# Function to plot 3D mesh with no outline and clean white color
def plot_mesh(mesh_obj):
    vertices = mesh_obj.vertices
    faces = mesh_obj.faces

    # Pure white color with a bit of transparency
    mesh_collection = Poly3DCollection(
        vertices[faces],
        facecolors=(1, 1, 1, 0.95),  # RGBA: white, slightly transparent
        edgecolors=(0, 0, 0, 0),     # Fully transparent edges
        linewidths=0,
        antialiased=False
    )

    ax.add_collection3d(mesh_collection)
    return vertices

# Extract all geometry components
def extract_all_geometries(obj):
    if isinstance(obj, trimesh.Scene):
        return list(obj.dump())
    elif isinstance(obj, list):
        return obj
    else:
        return [obj]

geometries = extract_all_geometries(loaded)

# Loop to generate rotating view images
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
