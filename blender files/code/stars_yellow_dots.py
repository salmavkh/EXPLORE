import bpy
import random

# Process:
# 1. Set a boundary and create a yellow material for the dots.
# 2. Randomly position each dot (tiny sphere) within the boundary.
# 3. Assign the yellow material to each dot and create 100 dots.

# Clear existing objects
#bpy.ops.object.select_all(action='SELECT')
#bpy.ops.object.delete(use_global=False)

# Set boundary dimensions (3D rectangular cube)
x_min, x_max = -5, 5
y_min, y_max = -5, 5
z_min, z_max = -5, 5

# Number of dots (stars) to generate
num_dots = 100

# Size of each dot (tiny sphere)
dot_radius = 0.1

# Create a basic yellow material
yellow_material = bpy.data.materials.new(name="YellowMaterial")
yellow_material.diffuse_color = (1, 1, 0, 1)  # Yellow color

# Function to create a dot (tiny sphere) at a random location
def create_dot():
    # Randomize position within the defined boundary
    x = random.uniform(x_min, x_max)
    y = random.uniform(y_min, y_max)
    z = random.uniform(z_min, z_max)

    # Create the sphere (dot)
    bpy.ops.mesh.primitive_uv_sphere_add(radius=dot_radius, location=(x, y, z))
    dot = bpy.context.object

    # Assign yellow material to the dot
    dot.data.materials.append(yellow_material)

# Generate dots within the boundary
for _ in range(num_dots):
    create_dot()

