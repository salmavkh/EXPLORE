import bpy
import math

# Process
# 1. Define the knot's shape with a curve and add it to the scene.
# 2. Create a rainbow material using Blender’s shader nodes.
# 3. Assign the material to the knot curve for a colorful effect.
    
# Clear existing mesh objects
# bpy.ops.object.select_all(action='DESELECT')
# bpy.ops.object.select_by_type(type='MESH')
# bpy.ops.object.delete()

# Define the parameters for the knot
num_points = 500  # Number of points for the curve
p = 3  # Number of twists
q = 8  # Complexity of the knot
radius = 2  # Radius of the torus
tube_radius = 0.1  # Radius of the tube

# Create a new curve data object
curve_data = bpy.data.curves.new(name="KnotCurve", type='CURVE')
curve_data.dimensions = '3D'
curve_data.fill_mode = 'FULL'
curve_data.bevel_depth = 0.05  # Thickness of the curve

# Create a new spline in the curve object
spline = curve_data.splines.new(type='POLY')
spline.points.add(num_points - 1)  # Add points to the spline

# Generate parametric points for the toroidal knot curve
for i in range(num_points):
    t = 2 * math.pi * i / num_points  # Parametric variable
    x = (radius + math.cos(q * t)) * math.cos(p * t)
    y = (radius + math.cos(q * t)) * math.sin(p * t)
    z = math.sin(q * t)
    spline.points[i].co = (x, y, z, 1)  # Add the 4th coordinate as 1 (w-coordinate for homogeneous)

# Create a new object with the curve data
curve_obj = bpy.data.objects.new("KnotCurveObject", curve_data)

# Add the object to the scene
bpy.context.collection.objects.link(curve_obj)

# Set the curve's extrude and bevel properties to give it thickness
curve_obj.data.bevel_depth = 0.05
curve_obj.data.bevel_resolution = 5

# Create a new material with a rainbow-like gradient
material = bpy.data.materials.new(name="KnotMaterial")
material.use_nodes = True
nodes = material.node_tree.nodes
links = material.node_tree.links

# Remove the default shader
for node in nodes:
    nodes.remove(node)

# Add new shader nodes
output_node = nodes.new(type='ShaderNodeOutputMaterial')
diffuse_node = nodes.new(type='ShaderNodeBsdfDiffuse')
color_ramp = nodes.new(type='ShaderNodeValToRGB')
gradient_node = nodes.new(type='ShaderNodeTexGradient')
texture_coord_node = nodes.new(type='ShaderNodeTexCoord')
mapping_node = nodes.new(type='ShaderNodeMapping')

# Position nodes
output_node.location = (300, 0)
diffuse_node.location = (0, 0)
color_ramp.location = (-300, 0)
gradient_node.location = (-600, 0)
texture_coord_node.location = (-900, 0)
mapping_node.location = (-1200, 0)

# Create links between nodes
links.new(output_node.inputs[0], diffuse_node.outputs[0])  # Output to diffuse shader
links.new(diffuse_node.inputs[0], color_ramp.outputs[0])  # Diffuse color from color ramp
links.new(color_ramp.inputs[0], gradient_node.outputs[0])  # Gradient input to color ramp
links.new(gradient_node.inputs[0], mapping_node.outputs[0])  # Mapping to gradient texture
links.new(mapping_node.inputs[0], texture_coord_node.outputs[3])  # Use object coordinates

# Assign color stops for a rainbow gradient
color_ramp.color_ramp.elements.new(0.25).color = (1, 0, 0, 1)  # Red
color_ramp.color_ramp.elements.new(0.50).color = (0, 1, 0, 1)  # Green
color_ramp.color_ramp.elements.new(0.75).color = (0, 0, 1, 1)  # Blue
color_ramp.color_ramp.elements[0].color = (1, 1, 0, 1)  # Yellow

# Assign the material to the curve object
curve_obj.data.materials.append(material)