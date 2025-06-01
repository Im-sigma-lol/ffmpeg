import trimesh
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection, Line3DCollection
import os
import numpy as np

path = '/storage/emulated/0/math/model.glb'
loaded = trimesh.load(path)

# Prepare output
output_dir = '/storage/emulated/0/math/frames/'
os.makedirs(output_dir, exist_ok=True)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.axis('off')

def plot_path3d(path_obj):
    for entity in path_obj.entities:
        points = path_obj.vertices[entity.points]
        ax.add_collection3d(Line3DCollection([points], colors='cyan', linewidths=1.5))
    return path_obj.vertices

def plot_mesh(mesh_obj):
    vertices = mesh_obj.vertices
    faces = mesh_obj.faces
    mesh_collection = Poly3DCollection(vertices[faces], alpha=0.9)
    mesh_collection.set_facecolor((0.5, 0.5, 1, 1))
    ax.add_collection3d(mesh_collection)
    return vertices

# Helper to extract individual objects from Scene/list/single
def extract_all_geometries(obj):
    if isinstance(obj, trimesh.Scene):
        return list(obj.dump())
    elif isinstance(obj, list):
        return obj
    else:
        return [obj]

geometries = extract_all_geometries(loaded)

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

    # Compute global scale
    if all_vertices:
        combined_vertices = np.vstack(all_vertices)
        scale = combined_vertices.flatten()
        ax.auto_scale_xyz(scale, scale, scale)

    ax.view_init(elev=30, azim=angle)

    frame_path = os.path.join(output_dir, f'frame_{i:03d}.png')
    plt.savefig(frame_path, dpi=200, transparent=True, bbox_inches='tight', pad_inches=0)
