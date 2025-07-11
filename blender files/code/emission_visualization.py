import sys
# Add the user site-packages path manually
sys.path.append("/Users/salmavkh/.local/lib/python3.11/site-packages")
# Import pandas
import pandas as pd
# Verify pandas installation
#print(pd.__version__)  # This should print the installed pandas version if successful
import bpy
import os

# Process
# 1. Total emission data is 2508 and there unique values of 208 (country)
# 2. Group by 208 country
# 3. Average the emission for each country
# 4. Put the data in the array
# 5. Loop: set the starting materials, create a new one, put the emission values on each cubes


# ------------------------ Load and process the data ------------------------
# Get the current directory where the Blender file is saved
blend_file_directory = bpy.path.abspath("//")
# CSV is in the same directory as the .blend file, set the path
csv_file_path = os.path.join(blend_file_directory, 'dataset/greenhouse.csv')
# Load the CSV file
df = pd.read_csv(csv_file_path)

# Step 1: Group by 'Federal organization' and calculate the mean of 'Emissions (kt)'
emission_means = df.groupby('Federal organization')['Emissions (kt)'].mean()
# Step 2: Normalize the mean values between 0 and 1
emission_means_normalized = (emission_means - emission_means.min()) / (emission_means.max() - emission_means.min())
# Step 3: Convert to a list and insert a 0 at the beginning to get 28 values
roughness_values = [0] + emission_means_normalized.tolist()


# ------------------------ Apply to the materials ------------------------
# Step 4: Now apply the calculated roughness values in the Blender scene
# Get the base material "Material.002"
base_material = bpy.data.materials.get("Material.002")

if base_material and base_material.use_nodes:
    # Count how many cubes have been processed
    cube_count = 0
    # Loop through each cube object and assign a unique material with a different roughness
    for obj in bpy.data.objects:
        if obj.type == 'MESH' and "Cube" in obj.name:
            # Ensure we do not exceed the roughness array size
            if cube_count < len(roughness_values):
                # Duplicate the base material
                new_material = base_material.copy()
                new_material.name = f"Material_{cube_count+1}"  # Give it a unique name 

                # Find the Glass BSDF node in the new material
                nodes = new_material.node_tree.nodes
                glass_bsdf = None
                for node in nodes:
                    if node.type == 'BSDF_GLASS':
                        glass_bsdf = node
                        break

                if glass_bsdf:
                    # Set the roughness for this specific cube
                    glass_bsdf.inputs['Roughness'].default_value = roughness_values[cube_count]
                    # Assign the new material to the object
                    if obj.data.materials:
                        obj.data.materials[0] = new_material  # Replace existing material
                    else:
                        obj.data.materials.append(new_material)  # Add new material
                    cube_count += 1
                else:
                    print(f"Glass BSDF node not found in material {new_material.name}")
            else:
                print(f"Exceeded the roughness array size for {obj.name}")
    print(f"Total cubes processed: {cube_count}")

else:
    print("Base material 'Material.002' not found or it does not use nodes.")