import gmsh
import sys

import numpy as np

# SETUP VARIABLES
d = 1.
h_over_d = 0.2
export_mesh = True


gmsh.initialize()

gmsh.model.add('mesh')
lc = 1e-2

center = (0, 0, 0)  # Do not change
inlet_x = -2.5 * d
bottom_wall_y = center[1] - d / 2 - h_over_d * d
outlet_x = 10 * d
upper_y = 3 * d

n_points = 1
n_curves = 1

# INNER CIRCLE
gmsh.model.geo.addPoint(center[0], center[1], center[2], lc, n_points)
n_points += 1
gmsh.model.geo.addPoint(center[0] + d / 2, center[1], center[2], lc, n_points)
n_points += 1

n_semi_circ_points = 2
initial_arc_angle = np.pi / (n_semi_circ_points * 2)
for i in range(n_semi_circ_points):
    gmsh.model.geo.addPoint(d / 2 * np.cos(i * np.pi / n_semi_circ_points + initial_arc_angle),
                            d / 2 * np.sin(i * np.pi / n_semi_circ_points + initial_arc_angle),
                            0, lc, n_points)
    gmsh.model.geo.addCircleArc(n_points - 1, 1, n_points, n_curves)
    n_points += 1
    n_curves += 1

gmsh.model.geo.addPoint(center[0] - d / 2, center[1], center[2], lc, n_points)
gmsh.model.geo.addCircleArc(n_points - 1, 1, n_points, n_curves)
n_points += 1
n_curves += 1

for i in range(n_semi_circ_points, 2 * n_semi_circ_points):
    gmsh.model.geo.addPoint(d / 2 * np.cos(i * np.pi / n_semi_circ_points + initial_arc_angle),
                            d / 2 * np.sin(i * np.pi / n_semi_circ_points + initial_arc_angle),
                            0, lc, n_points)
    gmsh.model.geo.addCircleArc(n_points - 1, 1, n_points, n_curves)
    n_points += 1
    n_curves += 1

gmsh.model.geo.addCircleArc(n_points - 1, 1, 2, n_curves)
n_curves += 1


# OUTER CIRCLE
intersection_angle = np.pi / 3


def intersection(y):
    return y / np.tan(intersection_angle)


gmsh.model.geo.addPoint(inlet_x, bottom_wall_y, 0, lc, n_points)
n_points += 1
gmsh.model.geo.addPoint(intersection(bottom_wall_y), bottom_wall_y, 0, lc, n_points)
gmsh.model.geo.addLine(n_points - 1, n_points, n_curves)
closest_point_index = 2 + n_semi_circ_points + 1 + n_semi_circ_points // 2
gmsh.model.geo.addLine(closest_point_index, n_points, n_curves + 1)
n_points += 1
n_curves += 2

radius = np.sqrt(intersection(bottom_wall_y) ** 2 + bottom_wall_y ** 2)
gmsh.model.geo.addPoint(center[0] - radius, center[1], 0, lc, n_points)
gmsh.model.geo.addCircleArc(n_points - 1, 1, n_points, n_curves)
n_points += 1
n_curves += 1

for i in range(n_semi_circ_points):
    gmsh.model.geo.addPoint(-radius * np.cos(i * np.pi / n_semi_circ_points + initial_arc_angle),
                            radius * np.sin(i * np.pi / n_semi_circ_points + initial_arc_angle),
                            0, lc, n_points)
    gmsh.model.geo.addCircleArc(n_points - 1, 1, n_points, n_curves)
    n_points += 1
    n_curves += 1

gmsh.model.geo.addPoint(center[0] + radius, center[1], 0, lc, n_points)
gmsh.model.geo.addCircleArc(n_points - 1, 1, n_points, n_curves)
n_points += 1
n_curves += 1

gmsh.model.geo.addPoint(-intersection(bottom_wall_y), bottom_wall_y, 0, lc, n_points)
gmsh.model.geo.addCircleArc(n_points - 1, 1, n_points, n_curves)
gmsh.model.geo.addLine(closest_point_index + 1, n_points, n_curves + 1)
n_points += 1
n_curves += 2

gmsh.model.geo.addLine(9, 14, n_curves)
n_curves += 1

gmsh.model.geo.addPoint(outlet_x, bottom_wall_y, 0, lc, n_points)
gmsh.model.geo.addLine(n_points - 1, n_points, n_curves)
n_points += 1
n_curves += 1

gmsh.model.geo.addPoint(outlet_x, center[1], 0, lc, n_points)
gmsh.model.geo.addLine(n_points - 1, n_points, n_curves)
n_points += 1
n_curves += 1

gmsh.model.geo.addLine(13, 16, n_curves)
gmsh.model.geo.addLine(2, 13, n_curves + 1)
n_curves += 2

upper_offset = 0.5 * d / 2
gmsh.model.geo.addPoint(outlet_x, center[1] + radius * np.sin(initial_arc_angle) + upper_offset, 0, lc, n_points)
gmsh.model.geo.addLine(n_points - 1, n_points, n_curves)
n_points += 1
n_curves += 1

gmsh.model.geo.addLine(12, n_points - 1, n_curves)
gmsh.model.geo.addLine(3, 12, n_curves + 1)
n_curves += 2

gmsh.model.geo.addPoint(outlet_x, upper_y, 0, lc, n_points)
gmsh.model.geo.addLine(n_points - 1, n_points, n_curves)
n_points += 1
n_curves += 1

horizontal_offset = 0.5 * d
gmsh.model.geo.addPoint(intersection(upper_y) - horizontal_offset, upper_y, 0, lc, n_points)
gmsh.model.geo.addLine(n_points, n_points - 1, n_curves)
gmsh.model.geo.addLine(12, n_points, n_curves + 1)
n_points += 1
n_curves += 2

gmsh.model.geo.addPoint(-intersection(upper_y) + horizontal_offset, upper_y, 0, lc, n_points)
gmsh.model.geo.addLine(n_points, n_points - 1, n_curves)
gmsh.model.geo.addLine(11, n_points, n_curves + 1)
gmsh.model.geo.addLine(4, 11, n_curves + 2)
n_points += 1
n_curves += 3

gmsh.model.geo.addPoint(inlet_x, upper_y, 0, lc, n_points)
gmsh.model.geo.addLine(n_points, n_points - 1, n_curves)
n_points += 1
n_curves += 1

gmsh.model.geo.addPoint(inlet_x, center[1] + radius * np.sin(initial_arc_angle) + upper_offset, 0, lc, n_points)
gmsh.model.geo.addLine(n_points, n_points - 1, n_curves)
gmsh.model.geo.addLine(n_points, 11, n_curves + 1)
n_points += 1
n_curves += 2

gmsh.model.geo.addPoint(inlet_x, center[1], 0, lc, n_points)
gmsh.model.geo.addLine(n_points, n_points - 1, n_curves)
gmsh.model.geo.addLine(n_points, 10, n_curves + 1)
gmsh.model.geo.addLine(10, 5, n_curves + 2)
gmsh.model.geo.addLine(n_points, 8, n_curves + 3)
n_points += 1
n_curves += 2


# MESHING
n_points = 36
mesh_type = 'Progression'
coef = 1.0
gmsh.model.geo.mesh.setTransfiniteCurve(1, n_points, mesh_type, coef)
gmsh.model.geo.mesh.setTransfiniteCurve(12, n_points, mesh_type, coef)
gmsh.model.geo.mesh.setTransfiniteCurve(20, n_points, mesh_type, coef)

n_points = 48
mesh_type = 'Progression'
coef = 1.0
gmsh.model.geo.mesh.setTransfiniteCurve(2, n_points, mesh_type, coef)
gmsh.model.geo.mesh.setTransfiniteCurve(11, n_points, mesh_type, coef)
gmsh.model.geo.mesh.setTransfiniteCurve(26, n_points, mesh_type, coef)

n_points = 24
mesh_type = 'Progression'
coef = 1.0
gmsh.model.geo.mesh.setTransfiniteCurve(3, n_points, mesh_type, coef)
gmsh.model.geo.mesh.setTransfiniteCurve(10, n_points, mesh_type, coef)
gmsh.model.geo.mesh.setTransfiniteCurve(32, n_points, mesh_type, coef)

n_points = 36
mesh_type = 'Progression'
coef = 1.02
gmsh.model.geo.mesh.setTransfiniteCurve(4, n_points, mesh_type, coef)
gmsh.model.geo.mesh.setTransfiniteCurve(9, n_points, mesh_type, coef)
gmsh.model.geo.mesh.setTransfiniteCurve(35, n_points, mesh_type, coef)

n_points = 48
mesh_type = 'Progression'
coef = 1.0
gmsh.model.geo.mesh.setTransfiniteCurve(5, n_points, mesh_type, coef)
gmsh.model.geo.mesh.setTransfiniteCurve(15, n_points, mesh_type, coef)

n_points = 48
mesh_type = 'Progression'
coef = 1.01
gmsh.model.geo.mesh.setTransfiniteCurve(6, n_points, mesh_type, coef)
gmsh.model.geo.mesh.setTransfiniteCurve(13, n_points, mesh_type, -coef)
gmsh.model.geo.mesh.setTransfiniteCurve(17, n_points, mesh_type, coef)

n_points = 48
mesh_type = 'Progression'
coef = 1.0
gmsh.model.geo.mesh.setTransfiniteCurve(19, n_points, mesh_type, coef)
gmsh.model.geo.mesh.setTransfiniteCurve(22, n_points, mesh_type, coef)
gmsh.model.geo.mesh.setTransfiniteCurve(28, n_points, mesh_type, coef)
gmsh.model.geo.mesh.setTransfiniteCurve(34, n_points, mesh_type, coef)
gmsh.model.geo.mesh.setTransfiniteCurve(8, n_points, mesh_type, coef)
gmsh.model.geo.mesh.setTransfiniteCurve(14, n_points, mesh_type, coef)

n_points = 48
mesh_type = 'Progression'
coef = 1.04
gmsh.model.geo.mesh.setTransfiniteCurve(30, n_points, mesh_type, coef)
gmsh.model.geo.mesh.setTransfiniteCurve(27, n_points, mesh_type, coef)
gmsh.model.geo.mesh.setTransfiniteCurve(25, n_points, mesh_type, coef)
gmsh.model.geo.mesh.setTransfiniteCurve(23, n_points, mesh_type, coef)

n_points = 48
mesh_type = 'Progression'
coef = -1.03
gmsh.model.geo.mesh.setTransfiniteCurve(29, n_points, mesh_type, coef)
gmsh.model.geo.mesh.setTransfiniteCurve(31, n_points, mesh_type, coef)
gmsh.model.geo.mesh.setTransfiniteCurve(33, n_points, mesh_type, coef)
gmsh.model.geo.mesh.setTransfiniteCurve(7, n_points, mesh_type, coef)

n_points = 96
mesh_type = 'Progression'
coef = 1.03
gmsh.model.geo.mesh.setTransfiniteCurve(24, n_points, mesh_type, coef)
gmsh.model.geo.mesh.setTransfiniteCurve(21, n_points, mesh_type, coef)
gmsh.model.geo.mesh.setTransfiniteCurve(18, n_points, mesh_type, coef)
gmsh.model.geo.mesh.setTransfiniteCurve(16, n_points, mesh_type, coef)

gmsh.model.geo.addCurveLoop([-29, -30, 31, 27], 1)
gmsh.model.geo.addPlaneSurface([1], 1)

gmsh.model.geo.addCurveLoop([-26, -27, 11, 25], 2)
gmsh.model.geo.addPlaneSurface([2], 2)

gmsh.model.geo.addCurveLoop([-24, -25, 21, 23], 3)
gmsh.model.geo.addPlaneSurface([3], 3)

gmsh.model.geo.addCurveLoop([-31, -32, 33, 10], 4)
gmsh.model.geo.addPlaneSurface([4], 4)

gmsh.model.geo.addCurveLoop([28, -10, 34, -3], 5)
gmsh.model.geo.addPlaneSurface([5], 5)

gmsh.model.geo.addCurveLoop([-11, -28, -2, 22], 6)
gmsh.model.geo.addPlaneSurface([6], 6)

gmsh.model.geo.addCurveLoop([-22, -1, 19, -12], 7)
gmsh.model.geo.addPlaneSurface([7], 7)

gmsh.model.geo.addCurveLoop([-21, 12, 18, 20], 8)
gmsh.model.geo.addPlaneSurface([8], 8)

gmsh.model.geo.addCurveLoop([-33, 35, 7, 9], 9)
gmsh.model.geo.addPlaneSurface([9], 9)

gmsh.model.geo.addCurveLoop([-34, -9, -8, -4], 10)
gmsh.model.geo.addPlaneSurface([10], 10)

gmsh.model.geo.addCurveLoop([-5, 8, 15, -14], 11)
gmsh.model.geo.addPlaneSurface([11], 11)

gmsh.model.geo.addCurveLoop([-19, -6, 14, -13], 12)
gmsh.model.geo.addPlaneSurface([12], 12)

gmsh.model.geo.addCurveLoop([-18, 13, 16, 17], 13)
gmsh.model.geo.addPlaneSurface([13], 13)

for i in range(1, 14):
    gmsh.model.geo.mesh.setTransfiniteSurface(i)
    gmsh.model.geo.mesh.setRecombine(2, i)

if export_mesh is True:
    # Generate dimTags
    dimtags = []
    for i in range(1, 14):
        dimtags.append((2, i))

    gmsh.model.geo.extrude(dimtags, 0, 0, 1, numElements=[1], recombine=True)

    gmsh.model.geo.addPhysicalGroup(2, [224, 114, 48, 44, 66, 88], 1000, 'Inlet')
    gmsh.model.geo.addPhysicalGroup(2, [100, 210, 320], 1001, 'Outlet')
    gmsh.model.geo.addPhysicalGroup(2, [228, 272, 316], 1002, 'Wall')
    gmsh.model.geo.addPhysicalGroup(2, [57, 79, 101, 211, 321, 123, 233, 255, 145, 167, 189, 299, 277, 1, 2, 3,
                                        4, 5, 6, 7, 8, 9, 10, 11, 12, 13], 1003, 'Side')
    gmsh.model.geo.addPhysicalGroup(2, [264, 254, 144, 162, 180, 290], 1004, 'Cylinder')
    gmsh.model.geo.addPhysicalGroup(3, [i for i in range(1, 14)], 1005, 'Fluid')

gmsh.model.geo.synchronize()

if export_mesh:
    gmsh.model.mesh.generate(3)
    gmsh.write('mesh.msh')

gmsh.fltk.run()

gmsh.finalize()
