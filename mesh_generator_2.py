import gmsh
import sys
from helper import *
import math
import numpy as np

# SETUP VARIABLES
Re = 4e4
D = 1.0
rho = 1.0

Uinf = math.sqrt(1.4) * 0.15  # nondimensional
Cf = (2 * math.log10(Re) - 0.65)**(-2.3)
utau = Uinf * math.sqrt(Cf / 2)
mu = Uinf * D * rho / Re
nu = mu / rho

viscous_length_scale = nu / utau
yplus_target_cyl = 0.7
yplus_target_wall = 2.0

ymin_cyl = yplus_target_cyl * viscous_length_scale
ymin_wall = yplus_target_wall * viscous_length_scale


# p = 101325
# R = 287.05
# T = 293
# rho = p / (R * T)
# mu = 1.812e-5
# M = 0.15
# a = np.sqrt(1.4 * R * T)
# d = Re * mu / (rho * M * a)

filename = 'mesh_wide.msh'

d = 1.
h_over_d = 0.4
export_mesh = True

gmsh.initialize()

gmsh.model.add('mesh')
lc = 1e-2

center = (0, 0, 0)  # Do not change
inlet_x = -5.0 * d
bottom_wall_y = center[1] - d / 2 - h_over_d * d
outlet_x = 20 * d
upper_y = 4.0 * d

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
offset = 0.5

for i in range(1, 4):
    gmsh.model.geo.addPoint(center[0] + radius * np.cos(i * np.pi / 2 + np.pi / 4),
                            center[1] + radius * np.sin(i * np.pi / 2 + np.pi / 4), center[2], lc, n_points)
    if i == 1:
        gmsh.model.geo.addPoint(center[0], center[1] - offset, center[2], lc, 8522)
        gmsh.model.geo.addCircleArc(n_points - 1, 8522, n_points, n_curves)
    if i == 2:
        gmsh.model.geo.addPoint(center[0] + offset, center[1], center[2], lc, 8523)
        gmsh.model.geo.addCircleArc(n_points - 1, 8523, n_points, n_curves)
    if i == 3:
        gmsh.model.geo.addPoint(center[0], center[1] + offset, center[2], lc, 8524)
        gmsh.model.geo.addCircleArc(n_points - 1, 8524, n_points, n_curves)

    n_points += 1
    n_curves += 1

gmsh.model.geo.addPoint(center[0] - offset, center[1], center[2], lc, 8525)
gmsh.model.geo.addCircleArc(n_points - 1, 8525, 6, n_curves)
n_curves += 1

for i in range(4):
    gmsh.model.geo.addLine(i + 2, i + 6, n_curves)
    n_curves += 1

gmsh.model.geo.addPoint(inlet_x, bottom_wall_y, 0, lc, n_points)
n_points += 1
gmsh.model.geo.addPoint(inlet_x, center[1] - radius * 0.7, 0, lc, n_points)
n_points += 1
gmsh.model.geo.addPoint(center[0] - radius * np.cos(3 * np.pi / 2 + np.pi / 3.5), bottom_wall_y, 0, lc, n_points)
n_points += 1
gmsh.model.geo.addLine(10, 12, n_curves)
n_curves += 1
gmsh.model.geo.addLine(12, 8, n_curves)
n_curves += 1
gmsh.model.geo.addLine(8, 11, n_curves)
n_curves += 1
gmsh.model.geo.addLine(11, 10, n_curves)
n_curves += 1

gmsh.model.geo.addPoint(center[0] + radius * np.cos(3 * np.pi / 2 + np.pi / 3.5), bottom_wall_y, 0, lc, n_points)
n_points += 1
gmsh.model.geo.addLine(12, 13, n_curves)
n_curves += 1
gmsh.model.geo.addLine(13, 9, n_curves)
n_curves += 1

gmsh.model.geo.addPoint(outlet_x, bottom_wall_y, 0, lc, n_points)
n_points += 1
gmsh.model.geo.addPoint(outlet_x, center[1] - radius * 0.5, 0, lc, n_points)
n_points += 1
gmsh.model.geo.addLine(13, 14, n_curves)
n_curves += 1
gmsh.model.geo.addLine(14, 15, n_curves)
n_curves += 1
gmsh.model.geo.addLine(15, 9, n_curves)
n_curves += 1

gmsh.model.geo.addPoint(outlet_x, center[1] + radius * 1.4, 0, lc, n_points)
n_points += 1
gmsh.model.geo.addLine(15, 16, n_curves)
n_curves += 1
gmsh.model.geo.addLine(16, 6, n_curves)
n_curves += 1

gmsh.model.geo.addPoint(outlet_x, upper_y, 0, lc, n_points)
n_points += 1
gmsh.model.geo.addPoint(center[0] + radius * 1.5, upper_y, 0, lc, n_points)
n_points += 1
gmsh.model.geo.addLine(16, 17, n_curves)
n_curves += 1
gmsh.model.geo.addLine(17, 18, n_curves)
n_curves += 1
gmsh.model.geo.addLine(18, 6, n_curves)
n_curves += 1

gmsh.model.geo.addPoint(center[0] - radius * 1.2, upper_y, 0, lc, n_points)
n_points += 1
gmsh.model.geo.addLine(18, 19, n_curves)
n_curves += 1
gmsh.model.geo.addLine(19, 7, n_curves)
n_curves += 1

gmsh.model.geo.addPoint(inlet_x, upper_y, 0, lc, n_points)
n_points += 1
gmsh.model.geo.addPoint(inlet_x, center[1] + radius * 1.2, 0, lc, n_points)
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
ncyl = 3500
nrad = 700
nwall = 1200
nupper = 800
ninlet = 1200
nwake = 1200

refinement = 0.1
n_points = int(ncyl / 4 * refinement)
mesh_type = 'Progression'
coef = 1.0
gmsh.model.geo.mesh.setTransfiniteCurve(1, n_points, mesh_type, coef)
gmsh.model.geo.mesh.setTransfiniteCurve(5, n_points, mesh_type, coef)
gmsh.model.geo.mesh.setTransfiniteCurve(27, n_points, mesh_type, coef)

n_points = int(ncyl / 4 * refinement)
mesh_type = 'Progression'
coef = -1.0
gmsh.model.geo.mesh.setTransfiniteCurve(3, n_points, mesh_type, coef)
gmsh.model.geo.mesh.setTransfiniteCurve(7, n_points, mesh_type, coef)
gmsh.model.geo.mesh.setTransfiniteCurve(17, n_points, mesh_type, coef)

n_points = int(ncyl / 4 * refinement)
mesh_type = 'Progression'
coef = 1.0
gmsh.model.geo.mesh.setTransfiniteCurve(32, n_points, mesh_type, coef)
gmsh.model.geo.mesh.setTransfiniteCurve(6, n_points, mesh_type, coef)
gmsh.model.geo.mesh.setTransfiniteCurve(2, n_points, mesh_type, coef)

n_points = int(ncyl / 4 * refinement)
mesh_type = 'Progression'
coef = 1.0
gmsh.model.geo.mesh.setTransfiniteCurve(4, n_points, mesh_type, coef)
gmsh.model.geo.mesh.setTransfiniteCurve(8, n_points, mesh_type, coef)
gmsh.model.geo.mesh.setTransfiniteCurve(22, n_points, mesh_type, coef)

# RADIAL AROUND CYLINDER
n_points = int(nrad * refinement)
mesh_type = 'Progression'
coef = r_from_ymin(ymin_cyl, radius - D/2, n_points)
ymax_cyl = ymin_cyl * coef ** (n_points-1)
print(coef)
gmsh.model.geo.mesh.setTransfiniteCurve(9, n_points, mesh_type, coef)
gmsh.model.geo.mesh.setTransfiniteCurve(10, n_points, mesh_type, coef)
gmsh.model.geo.mesh.setTransfiniteCurve(11, n_points, mesh_type, coef)
gmsh.model.geo.mesh.setTransfiniteCurve(12, n_points, mesh_type, coef)

# NORMAL NEAR THE WALL
n_points = int(nwall * refinement)
mesh_type = 'Progression'
coef = r_from_ymin(ymin_wall, D * (1 + h_over_d) - radius, n_points)
print(coef)
gmsh.model.geo.mesh.setTransfiniteCurve(16, n_points, mesh_type, -coef)
gmsh.model.geo.mesh.setTransfiniteCurve(14, n_points, mesh_type, coef)
gmsh.model.geo.mesh.setTransfiniteCurve(18, n_points, mesh_type, coef)
gmsh.model.geo.mesh.setTransfiniteCurve(20, n_points, mesh_type, coef)

n_points = int(nupper * refinement)
mesh_type = 'Progression'
coef = -r_from_ymin(ymax_cyl, abs(upper_y - radius), n_points) - 0.005
gmsh.model.geo.mesh.setTransfiniteCurve(30, n_points, mesh_type, coef)
gmsh.model.geo.mesh.setTransfiniteCurve(28, n_points, mesh_type, coef)
gmsh.model.geo.mesh.setTransfiniteCurve(26, n_points, mesh_type, coef)
gmsh.model.geo.mesh.setTransfiniteCurve(24, n_points, mesh_type, 1.0)

n_points = int(ninlet * refinement)
mesh_type = 'Progression'
coef = -r_from_ymin(ymax_cyl, abs(inlet_x - radius), n_points)
gmsh.model.geo.mesh.setTransfiniteCurve(29, n_points, mesh_type, -coef)
gmsh.model.geo.mesh.setTransfiniteCurve(31, n_points, mesh_type, coef)
gmsh.model.geo.mesh.setTransfiniteCurve(15, n_points, mesh_type, -coef)
gmsh.model.geo.mesh.setTransfiniteCurve(13, n_points, mesh_type, coef)

n_points = int(nwake * refinement)
mesh_type = 'Progression'
coef = -r_from_ymin(ymax_cyl, abs(outlet_x - radius), n_points) + 0.001
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

    gmsh.model.geo.extrude(dimtags, 0, 0, 0.01, numElements=[1], recombine=True)

    gmsh.model.geo.addPhysicalGroup(2, [41, 199, 181], 1000, 'Inlet')
    gmsh.model.geo.addPhysicalGroup(2, [177, 159, 137], 1006, 'Top')
    gmsh.model.geo.addPhysicalGroup(2, [89, 111, 133], 1001, 'Outlet')
    gmsh.model.geo.addPhysicalGroup(2, [45, 85, 63], 1002, 'Wall')
    gmsh.model.geo.addPhysicalGroup(2, [186, 208, 54, 76, 98, 120, 142, 164, 230, 252, 274, 296, 1, 2, 3,
                                        4, 5, 6, 7, 8, 9, 10, 11, 12], 1003, 'Side')
    gmsh.model.geo.addPhysicalGroup(2, [217, 295, 251, 273], 1004, 'Cylinder')
    gmsh.model.geo.addPhysicalGroup(3, [i for i in range(1, 13)], 1005, 'Fluid')

gmsh.model.geo.synchronize()

if export_mesh:
    gmsh.model.mesh.generate(3)
    gmsh.write(filename)

gmsh.fltk.run()

gmsh.finalize()