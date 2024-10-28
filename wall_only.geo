SetFactory("OpenCASCADE");

//+
Point(1) = {-5, 0, 0, 1.0};
//+
Point(2) = {20, 0, 0, 1.0};
//+
Point(3) = {-5, 10, 0, 1.0};
//+
Point(4) = {20, 10, 0, 1.0};
//+
Line(1) = {1, 2};
//+
Line(2) = {1, 3};
//+
Line(3) = {3, 4};
//+
Line(4) = {2, 4};
//+
Transfinite Curve {2, 4} = 100 Using Progression 1.02;
//+
Transfinite Curve {1, 3} = 200 Using Progression 1;
//+
Curve Loop(1) = {1, 2, 3, 4};
//+
Plane Surface(1) = {1};
//+
Transfinite Surface {1};
//+
Recombine Surface {1};
//+
Extrude {0, 0, 1} {
  Surface{1}; Layers {1}; Recombine;
}
//+
Physical Volume("Fluid", 13) = {1};
//+
Physical Surface("Inlet", 14) = {5, 4};
//+
Physical Surface("Outlet", 15) = {3};
//+
Physical Surface("Side", 16) = {6, 1};
//+
Physical Surface("Wall", 17) = {2};
