import trimesh                              # For loading and working with 3D models
import matplotlib.pyplot as plt             # For plotting
from mpl_toolkits.mplot3d.art3d import Poly3DCollection, Line3DCollection  # For rendering 3D polygons and lines
import os                                   # For file and directory operations
import numpy as np                          # For handling numerical data

# Path to your 3D model file (GLB format)
path = '/storage/emulated/0/math/model.glb'

# Load the 3D model using trimesh
loaded = trimesh.load(path)

# Directory where rendered frames will be saved
output_dir = '/storage/emulated/0/math/frames/'
os.makedirs(output_dir, exist_ok=True)  # Create directory if it doesn't exist

# Set up a 3D figure using matplotlib
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.axis('off')  # Hide axis for cleaner output

# Function to render 3D line-based paths (for wireframe-type models or paths)
def plot_path3d(path_obj):
    for entity in path_obj.entities:
        # Extract line segment vertices from entity
        points = path_obj.vertices[entity.points]
        # Add the line collection to the plot
        ax.add_collection3d(Line3DCollection([points], colors='cyan', linewidths=1.5))
    return path_obj.vertices  # Return vertices for scaling

# Function to render solid 3D meshes
def plot_mesh(mesh_obj):
    vertices = mesh_obj.vertices  # 3D points
    faces = mesh_obj.faces        # Indexes into vertices forming triangles

    # Create a 3D polygon collection from faces, disabling edge outlines
    mesh_collection = Poly3DCollection(vertices[faces], alpha=0.9, edgecolors='none')
    mesh_collection.set_facecolor((0.5, 0.5, 1, 1))  # Set face color to bluish

    # Add the mesh to the plot
    ax.add_collection3d(mesh_collection)
    return vertices  # Return vertices for scaling

# Helper to extract all geometry objects (whether Scene, list, or single mesh)
def extract_all_geometries(obj):
    if isinstance(obj, trimesh.Scene):
        return list(obj.dump())  # Flatten all geometry from scene
    elif isinstance(obj, list):
        return obj              # Already a list of meshes
    else:
        return [obj]            # Single mesh or path

# Get a flat list of all geometry objects from the loaded file
geometries = extract_all_geometries(loaded)

# Loop through angles from 0 to 355 in steps of 5 to generate a turntable animation
for i, angle in enumerate(range(0, 360, 5)):
    ax.cla()        # Clear the axes
    ax.axis('off')  # Turn off the axis display
    all_vertices = []

    # Plot each geometry: mesh or path
    for geo in geometries:
        if isinstance(geo, trimesh.Trimesh):
            v = plot_mesh(geo)  # Plot solid mesh
        elif isinstance(geo, trimesh.path.path.Path3D):
            v = plot_path3d(geo)  # Plot line-based path
        else:
            continue
        all_vertices.append(v)  # Save vertices for global scaling

    # Auto-scale plot based on all vertex data
    if all_vertices:
        combined_vertices = np.vstack(all_vertices)  # Stack all vertices
        scale = combined_vertices.flatten()          # Flatten to 1D for scaling
        ax.auto_scale_xyz(scale, scale, scale)       # Set 3D scaling

    ax.view_init(elev=30, azim=angle)  # Rotate view: elevation 30°, azimuth varies

    # Save current frame to image file
    frame_path = os.path.join(output_dir, f'frame_{i:03d}.png')
    plt.savefig(frame_path, dpi=200, transparent=True, bbox_inches='tight', pad_inches=0)

# Optional: close the plot window after all frames are saved
plt.close(fig)
