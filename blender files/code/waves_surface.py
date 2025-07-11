import bpy
import math

# Process
# 1. Create a grid of vertices with a wave shape using math functions for height.
# 2. Define faces connecting the vertices to form a mesh grid.
# 3. Apply smooth shading to the wave object.

# Clear existing mesh data
#bpy.ops.object.select_all(action='DESELECT')
#bpy.ops.object.select_by_type(type='MESH')
#bpy.ops.object.delete()

# Define a new mesh and object
mesh = bpy.data.meshes.new(name='WaveMesh')
obj = bpy.data.objects.new('WaveObject', mesh)
bpy.context.collection.objects.link(obj)
bpy.context.view_layer.objects.active = obj
obj.select_set(True)

# Define parameters
size = 30          # Grid size
spacing = 0.5      # Spacing between grid points
height_scale = 0.8 # Height scale of the wave
wave_frequency = 5 # Frequency of the wave

# Create lists for vertices and faces
vertices = []
faces = []

# Create a grid of vertices using a mathematical function
for i in range(size):
    for j in range(size):
        x = i * spacing
        y = j * spacing
        z = math.sin(i * wave_frequency * 0.1) * math.cos(j * wave_frequency * 0.1) * height_scale
        vertices.append((x, y, z))

# Create faces based on grid
for i in range(size - 1):
    for j in range(size - 1):
        v1 = i * size + j
        v2 = v1 + 1
        v3 = v1 + size
        v4 = v3 + 1
        faces.append((v1, v2, v4, v3))

# Create the mesh from the vertices and faces
mesh.from_pydata(vertices, [], faces)
mesh.update()

# Set object properties
obj.location = (-size * spacing / 2, -size * spacing / 2, 0)  # Center the object
obj.scale = (1, 1, 1)

# Update the scene
bpy.context.view_layer.update()

# Optionally, set the material for a cool effect
material = bpy.data.materials.new(name="WaveMaterial")
material.use_nodes = True
bsdf = material.node_tree.nodes["Principled BSDF"]
bsdf.inputs["Base Color"].default_value = (0.1, 0.5, 1.0, 1)  # Cool blueish color
bsdf.inputs["Roughness"].default_value = 0.3
obj.data.materials.append(material)

# Set smooth shading
bpy.ops.object.shade_smooth()
bpy.context.view_layer.update()