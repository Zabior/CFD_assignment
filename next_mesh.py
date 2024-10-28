import gmsh

# Initialize Gmsh
gmsh.initialize()
gmsh.model.add("cylinder_boundary_layer")

# Parameters for the cylinder
radius = 1.0          # Cylinder radius
height = 5.0          # Length of the cylinder along the axis
mesh_size_far = 0.2   # Mesh size far from the wall
boundary_layer_thickness = 0.01  # Thickness of the boundary layer
n_boundary_layers = 5  # Number of boundary layers
growth_rate = 1.2      # Growth rate for boundary layers

# Create the cylinder
cylinder_center = [0, 0, 0]
cylinder_axis = [0, 0, 1]
cylinder_tag = gmsh.model.occ.addCylinder(cylinder_center[0], cylinder_center[1], cylinder_center[2],
                                           cylinder_axis[0], cylinder_axis[1], cylinder_axis[2],
                                           radius)

# Synchronize the CAD kernel with the Gmsh model
gmsh.model.occ.synchronize()

# Define mesh size far from the wall
gmsh.model.mesh.setSize(gmsh.model.getBoundary([(3, cylinder_tag)], oriented=False), mesh_size_far)

# Add boundary layer around the cylinder
cylinder_surface = gmsh.model.getBoundary([(3, cylinder_tag)], oriented=False, recursive=False)
gmsh.model.mesh.field.add("BoundaryLayer", 1)
gmsh.model.mesh.field.setNumbers(1, "FacesList", [s[1] for s in cylinder_surface])
gmsh.model.mesh.field.setNumber(1, "hwall_n", boundary_layer_thickness)
gmsh.model.mesh.field.setNumber(1, "thickness", boundary_layer_thickness)
gmsh.model.mesh.field.setNumber(1, "ratio", growth_rate)
gmsh.model.mesh.field.setNumber(1, "nLayers", n_boundary_layers)
gmsh.model.mesh.field.setAsBoundaryLayer(1)

# Generate the 3D mesh
gmsh.model.mesh.generate(3)

# Optionally save the mesh
gmsh.write("cylinder_boundary_layer.msh")

# Finalize Gmsh
gmsh.finalize()


gmsh.fltk.run()

gmsh.finalize()