import trimesh
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection, Line3DCollection
import os
import numpy as np

# Load path (use /sdcard instead of /storage/emulated/0 for Termux compatibility)
path = '/sdcard/math/model.glb'
loaded = trimesh.load(path)

# Output folder for frames
output_dir = '/sdcard/math/frames/'
os.makedirs(output_dir, exist_ok=True)

# Create 3D plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.axis('off')  # Turn off axis lines and labels

# Function to plot 3D line paths
def plot_path3d(path_obj):
    for entity in path_obj.entities:
        points = path_obj.vertices[entity.points]
        ax.add_collection3d(Line3DCollection([points], colors='cyan', linewidths=1.5))
    return path_obj.vertices

# Function to plot 3D mesh without outlines
def plot_mesh(mesh_obj):
    vertices = mesh_obj.vertices
    faces = mesh_obj.faces

    # Create the mesh collection with no edgecolor and transparent background
    mesh_collection = Poly3DCollection(vertices[faces], 
                                       facecolors=(0.5, 0.5, 1, 1),   # Light blue
                                       edgecolors='none',            # Disable outlines
                                       linewidths=0)                 # Force no outline width

    ax.add_collection3d(mesh_collection)
    return vertices

# Helper to extract all geometries from a scene or list
def extract_all_geometries(obj):
    if isinstance(obj, trimesh.Scene):
        return list(obj.dump())
    elif isinstance(obj, list):
        return obj
    else:
        return [obj]

# Extract all parts from model
geometries = extract_all_geometries(loaded)

# Generate frames while rotating the model
for i, angle in enumerate(range(0, 360, 5)):
    ax.cla()
    ax.axis('off')
    all_vertices = []

    # Plot all geometry objects
    for geo in geometries:
        if isinstance(geo, trimesh.Trimesh):
            v = plot_mesh(geo)
        elif isinstance(geo, trimesh.path.path.Path3D):
            v = plot_path3d(geo)
        else:
            continue
        all_vertices.append(v)

    # Autoscale scene based on combined vertices
    if all_vertices:
        combined = np.vstack(all_vertices)
        scale = combined.flatten()
        ax.auto_scale_xyz(scale, scale, scale)

    # Set the view angle for rotation animation
    ax.view_init(elev=30, azim=angle)

    # Save the frame image
    frame_path = os.path.join(output_dir, f'frame_{i:03d}.png')
    plt.savefig(frame_path, dpi=200, transparent=True, bbox_inches='tight', pad_inches=0)

# Optional: close the figure after rendering
plt.close(fig)import trimesh
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection, Line3DCollection
import os
import numpy as np

# Load path (use /sdcard instead of /storage/emulated/0 for Termux compatibility)
path = '/sdcard/math/model.glb'
loaded = trimesh.load(path)

# Output folder for frames
output_dir = '/sdcard/math/frames/'
os.makedirs(output_dir, exist_ok=True)

# Create 3D plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.axis('off')  # Turn off axis lines and labels

# Function to plot 3D line paths
def plot_path3d(path_obj):
    for entity in path_obj.entities:
        points = path_obj.vertices[entity.points]
        ax.add_collection3d(Line3DCollection([points], colors='cyan', linewidths=1.5))
    return path_obj.vertices

# Function to plot 3D mesh without outlines
def plot_mesh(mesh_obj):
    vertices = mesh_obj.vertices
    faces = mesh_obj.faces

    # Create the mesh collection with no edgecolor and transparent background
    mesh_collection = Poly3DCollection(vertices[faces], 
                                       facecolors=(0.5, 0.5, 1, 1),   # Light blue
                                       edgecolors='none',            # Disable outlines
                                       linewidths=0)                 # Force no outline width

    ax.add_collection3d(mesh_collection)
    return vertices

# Helper to extract all geometries from a scene or list
def extract_all_geometries(obj):
    if isinstance(obj, trimesh.Scene):
        return list(obj.dump())
    elif isinstance(obj, list):
        return obj
    else:
        return [obj]

# Extract all parts from model
geometries = extract_all_geometries(loaded)

# Generate frames while rotating the model
for i, angle in enumerate(range(0, 360, 5)):
    ax.cla()
    ax.axis('off')
    all_vertices = []

    # Plot all geometry objects
    for geo in geometries:
        if isinstance(geo, trimesh.Trimesh):
            v = plot_mesh(geo)
        elif isinstance(geo, trimesh.path.path.Path3D):
            v = plot_path3d(geo)
        else:
            continue
        all_vertices.append(v)

    # Autoscale scene based on combined vertices
    if all_vertices:
        combined = np.vstack(all_vertices)
        scale = combined.flatten()
        ax.auto_scale_xyz(scale, scale, scale)

    # Set the view angle for rotation animation
    ax.view_init(elev=30, azim=angle)

    # Save the frame image
    frame_path = os.path.join(output_dir, f'frame_{i:03d}.png')
    plt.savefig(frame_path, dpi=200, transparent=True, bbox_inches='tight', pad_inches=0)

# Optional: close the figure after rendering
plt.close(fig)
