import gmsh
import sys

import numpy as np

# SETUP VARIABLES
# Re = 4e4
# p = 101325
# R = 287.05
# T = 293
# rho = p / (R * T)
# mu = 1.812e-5
# M = 0.15
# a = np.sqrt(1.4 * R * T)
# d = Re * mu / (rho * M * a)
d = 1.
h_over_d = 0.4
export_mesh = True

gmsh.initialize()

gmsh.model.add('mesh')
lc = 1e-2

center = (0, 0, 0)  # Do not change
inlet_x = -2.5 * d
bottom_wall_y = center[1] - d / 2 - h_over_d * d
outlet_x = 12 * d
upper_y = 3 * d

n_points = 1
n_curves = 1

# INNER CIRCLE
gmsh.model.geo.addPoint(center[0], center[1], center[2], lc, n_points)
n_points += 1
gmsh.model.geo.addPoint(center[0] + d / 2 * np.cos(np.pi / 4),
                        center[1] + d / 2 * np.sin(np.pi / 4), center[2], lc, n_points)
n_points += 1

for i in range(1, 4):
    gmsh.model.geo.addPoint(center[0] + d / 2 * np.cos(i * np.pi / 2 + np.pi / 4),
                            center[1] + d / 2 * np.sin(i * np.pi / 2 + np.pi / 4), center[2], lc, n_points)
    gmsh.model.geo.addCircleArc(n_points - 1, 1, n_points, n_curves)
    n_points += 1
    n_curves += 1

gmsh.model.geo.addCircleArc(n_points - 1, 1, 2, n_curves)
n_curves += 1

radius = d / 2 * (1 + h_over_d)
gmsh.model.geo.addPoint(center[0] + radius * np.cos(np.pi / 4),
                        center[1] + radius * np.sin(np.pi / 4), center[2], lc, n_points)
n_points += 1

for i in range(1, 4):
    gmsh.model.geo.addPoint(center[0] + radius * np.cos(i * np.pi / 2 + np.pi / 4),
                            center[1] + radius * np.sin(i * np.pi / 2 + np.pi / 4), center[2], lc, n_points)
    gmsh.model.geo.addCircleArc(n_points - 1, 1, n_points, n_curves)
    n_points += 1
    n_curves += 1

gmsh.model.geo.addCircleArc(n_points - 1, 1, 6, n_curves)
n_curves += 1

for i in range(4):
    gmsh.model.geo.addLine(i + 2, i + 6, n_curves)
    n_curves += 1

gmsh.model.geo.addPoint(inlet_x, bottom_wall_y, 0, lc, n_points)
n_points += 1
gmsh.model.geo.addPoint(inlet_x, center[1] - radius, 0, lc, n_points)
n_points += 1
gmsh.model.geo.addPoint(center[0] - radius, bottom_wall_y, 0, lc, n_points)
n_points += 1
gmsh.model.geo.addLine(10, 12, n_curves)
n_curves += 1
gmsh.model.geo.addLine(12, 8, n_curves)
n_curves += 1
gmsh.model.geo.addLine(8, 11, n_curves)
n_curves += 1
gmsh.model.geo.addLine(11, 10, n_curves)
n_curves += 1

gmsh.model.geo.addPoint(center[0] + radius, bottom_wall_y, 0, lc, n_points)
n_points += 1
gmsh.model.geo.addLine(12, 13, n_curves)
n_curves += 1
gmsh.model.geo.addLine(13, 9, n_curves)
n_curves += 1

gmsh.model.geo.addPoint(outlet_x, bottom_wall_y, 0, lc, n_points)
n_points += 1
gmsh.model.geo.addPoint(outlet_x, center[1] - radius, 0, lc, n_points)
n_points += 1
gmsh.model.geo.addLine(13, 14, n_curves)
n_curves += 1
gmsh.model.geo.addLine(14, 15, n_curves)
n_curves += 1
gmsh.model.geo.addLine(15, 9, n_curves)
n_curves += 1

gmsh.model.geo.addPoint(outlet_x, center[1] + radius, 0, lc, n_points)
n_points += 1
gmsh.model.geo.addLine(15, 16, n_curves)
n_curves += 1
gmsh.model.geo.addLine(16, 6, n_curves)
n_curves += 1

gmsh.model.geo.addPoint(outlet_x, upper_y, 0, lc, n_points)
n_points += 1
gmsh.model.geo.addPoint(center[0] + radius, upper_y, 0, lc, n_points)
n_points += 1
gmsh.model.geo.addLine(16, 17, n_curves)
n_curves += 1
gmsh.model.geo.addLine(17, 18, n_curves)
n_curves += 1
gmsh.model.geo.addLine(18, 6, n_curves)
n_curves += 1

gmsh.model.geo.addPoint(center[0] - radius, upper_y, 0, lc, n_points)
n_points += 1
gmsh.model.geo.addLine(18, 19, n_curves)
n_curves += 1
gmsh.model.geo.addLine(19, 7, n_curves)
n_curves += 1

gmsh.model.geo.addPoint(inlet_x, upper_y, 0, lc, n_points)
n_points += 1
gmsh.model.geo.addPoint(inlet_x, center[1] + radius, 0, lc, n_points)
n_points += 1
gmsh.model.geo.addLine(19, 20, n_curves)
n_curves += 1
gmsh.model.geo.addLine(20, 21, n_curves)
n_curves += 1
gmsh.model.geo.addLine(21, 7, n_curves)
n_curves += 1

gmsh.model.geo.addLine(21, 11, n_curves)
n_curves += 1


# MESHING
refinement = 1.0
n_points = int(72 * refinement)
mesh_type = 'Progression'
coef = 1.0
gmsh.model.geo.mesh.setTransfiniteCurve(1, n_points, mesh_type, coef)
gmsh.model.geo.mesh.setTransfiniteCurve(5, n_points, mesh_type, coef)
gmsh.model.geo.mesh.setTransfiniteCurve(27, n_points, mesh_type, coef)

n_points = int(72 * refinement)
mesh_type = 'Progression'
coef = 1.0
gmsh.model.geo.mesh.setTransfiniteCurve(3, n_points, mesh_type, coef)
gmsh.model.geo.mesh.setTransfiniteCurve(7, n_points, mesh_type, coef)
gmsh.model.geo.mesh.setTransfiniteCurve(17, n_points, mesh_type, coef)

n_points = int(72 * refinement)
mesh_type = 'Progression'
coef = 1.0
gmsh.model.geo.mesh.setTransfiniteCurve(32, n_points, mesh_type, coef)
gmsh.model.geo.mesh.setTransfiniteCurve(6, n_points, mesh_type, coef)
gmsh.model.geo.mesh.setTransfiniteCurve(2, n_points, mesh_type, coef)

n_points = int(72 * refinement)
mesh_type = 'Progression'
coef = 1.0
gmsh.model.geo.mesh.setTransfiniteCurve(4, n_points, mesh_type, coef)
gmsh.model.geo.mesh.setTransfiniteCurve(8, n_points, mesh_type, coef)
gmsh.model.geo.mesh.setTransfiniteCurve(22, n_points, mesh_type, coef)

n_points = int(36 * refinement)
mesh_type = 'Progression'
coef = 1.01
gmsh.model.geo.mesh.setTransfiniteCurve(9, n_points, mesh_type, coef)
gmsh.model.geo.mesh.setTransfiniteCurve(10, n_points, mesh_type, coef)
gmsh.model.geo.mesh.setTransfiniteCurve(11, n_points, mesh_type, coef)
gmsh.model.geo.mesh.setTransfiniteCurve(12, n_points, mesh_type, coef)

n_points = int(48 * refinement)
mesh_type = 'Progression'
coef = 1.01
gmsh.model.geo.mesh.setTransfiniteCurve(16, n_points, mesh_type, coef)
gmsh.model.geo.mesh.setTransfiniteCurve(14, n_points, mesh_type, coef)
gmsh.model.geo.mesh.setTransfiniteCurve(18, n_points, mesh_type, coef)
gmsh.model.geo.mesh.setTransfiniteCurve(20, n_points, mesh_type, coef)

n_points = int(96 * refinement)
mesh_type = 'Progression'
coef = -1.035
gmsh.model.geo.mesh.setTransfiniteCurve(30, n_points, mesh_type, coef)
gmsh.model.geo.mesh.setTransfiniteCurve(28, n_points, mesh_type, coef)
gmsh.model.geo.mesh.setTransfiniteCurve(26, n_points, mesh_type, coef)
gmsh.model.geo.mesh.setTransfiniteCurve(24, n_points, mesh_type, -coef)

n_points = int(64 * refinement)
mesh_type = 'Progression'
coef = -1.045
gmsh.model.geo.mesh.setTransfiniteCurve(29, n_points, mesh_type, -coef)
gmsh.model.geo.mesh.setTransfiniteCurve(31, n_points, mesh_type, coef)
gmsh.model.geo.mesh.setTransfiniteCurve(15, n_points, mesh_type, -coef)
gmsh.model.geo.mesh.setTransfiniteCurve(13, n_points, mesh_type, coef)

n_points = int(240 * refinement)
mesh_type = 'Progression'
coef = -1.015
gmsh.model.geo.mesh.setTransfiniteCurve(25, n_points, mesh_type, coef)
gmsh.model.geo.mesh.setTransfiniteCurve(23, n_points, mesh_type, coef)
gmsh.model.geo.mesh.setTransfiniteCurve(21, n_points, mesh_type, coef)
gmsh.model.geo.mesh.setTransfiniteCurve(19, n_points, mesh_type, -coef)

gmsh.model.geo.addCurveLoop([16, 13, 14, 15], 1)
gmsh.model.geo.addPlaneSurface([1], 1)

gmsh.model.geo.addCurveLoop([17, 18, -7, -14], 2)
gmsh.model.geo.addPlaneSurface([2], 2)

gmsh.model.geo.addCurveLoop([19, 20, 21, -18], 3)
gmsh.model.geo.addPlaneSurface([3], 3)

gmsh.model.geo.addCurveLoop([-21, 22, 23, -8], 4)
gmsh.model.geo.addPlaneSurface([4], 4)

gmsh.model.geo.addCurveLoop([-23, 24, 25, 26], 5)
gmsh.model.geo.addPlaneSurface([5], 5)

gmsh.model.geo.addCurveLoop([-5, -26, 27, 28], 6)
gmsh.model.geo.addPlaneSurface([6], 6)

gmsh.model.geo.addCurveLoop([-28, 29, 30, 31], 7)
gmsh.model.geo.addPlaneSurface([7], 7)

gmsh.model.geo.addCurveLoop([-31, 32, -15, -6], 8)
gmsh.model.geo.addPlaneSurface([8], 8)

gmsh.model.geo.addCurveLoop([-1, 9, 5, -10], 9)
gmsh.model.geo.addPlaneSurface([9], 9)

gmsh.model.geo.addCurveLoop([10, 6, -11, -2], 10)
gmsh.model.geo.addPlaneSurface([10], 10)

gmsh.model.geo.addCurveLoop([11, 7, -12, -3], 11)
gmsh.model.geo.addPlaneSurface([11], 11)

gmsh.model.geo.addCurveLoop([12, 8, -9, -4], 12)
gmsh.model.geo.addPlaneSurface([12], 12)

#
for i in range(1, 13):
    gmsh.model.geo.mesh.setTransfiniteSurface(i)
    gmsh.model.geo.mesh.setRecombine(2, i)

if export_mesh is True:
    # Generate dimTags
    dimtags = []
    for i in range(1, 13):
        dimtags.append((2, i))

    gmsh.model.geo.extrude(dimtags, 0, 0, 1, numElements=[1], recombine=True)

    gmsh.model.geo.addPhysicalGroup(2, [41, 199, 181, 177, 159, 137], 1000, 'Inlet')
    gmsh.model.geo.addPhysicalGroup(2, [89, 111, 133], 1001, 'Outlet')
    gmsh.model.geo.addPhysicalGroup(2, [45, 85, 63], 1002, 'Wall')
    gmsh.model.geo.addPhysicalGroup(2, [186, 208, 54, 76, 98, 120, 142, 164, 230, 252, 274, 296, 1, 2, 3,
                                        4, 5, 6, 7, 8, 9, 10, 11, 12], 1003, 'Side')
    gmsh.model.geo.addPhysicalGroup(2, [217, 295, 251, 273], 1004, 'Cylinder')
    gmsh.model.geo.addPhysicalGroup(3, [i for i in range(1, 13)], 1005, 'Fluid')

gmsh.model.geo.synchronize()

if export_mesh:
    gmsh.model.mesh.generate(3)
    gmsh.write('mesh.msh')

gmsh.fltk.run()

gmsh.finalize()
