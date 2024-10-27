SetFactory("OpenCASCADE");
intArcPoint = 0.5*Sin(Pi/4);
extArcPoint = 0.6*Sin(Pi/4);
fac = 0.5;
ncyl = 200;
nr = 20;
ninlet = 250;
nwake = 180;
rr = 1.03259422;
rwake = 1.015;

//+
Point(1) = {intArcPoint, intArcPoint, 0, 1.0};
Point(2) = {-intArcPoint, intArcPoint, 0, 1.0};
Point(3) = {intArcPoint, -intArcPoint, 0, 1.0};
Point(4) = {-intArcPoint, -intArcPoint, 0, 1.0};
Point(5) = {0, 0, 0, 1.0};
//+
Circle(1) = {2, 5, 1};
//+
Circle(2) = {1, 5, 3};
//+
Circle(3) = {3, 5, 4};
//+
Circle(4) = {4, 5, 2};

Point(6) = {extArcPoint, extArcPoint, 0, 1.0};
Point(7) = {-extArcPoint, extArcPoint, 0, 1.0};
Point(8) = {extArcPoint, -extArcPoint, 0, 1.0};
Point(9) = {-extArcPoint, -extArcPoint, 0, 1.0};
//+
Circle(5) = {6, 5, 8};
//+
Circle(6) = {8, 5, 9};
//+
Circle(7) = {9, 5, 7};
//+
Circle(8) = {7, 5, 6};
//+
Line(9) = {2, 7};
//+
Line(10) = {1, 6};
//+
Line(11) = {3, 8};
//+
Line(12) = {4, 9};
//+
Point(10) = {(1 + fac) * extArcPoint, 5, 0, 1.0};
//+
Point(11) = {-(1 + fac) * extArcPoint, 5, 0, 1.0};
//+
Point(12) = {-(1 + fac) * extArcPoint, -0.9, 0, 1.0};
//+
Point(13) = {(1 + fac) * extArcPoint, -0.9, 0, 1.0};
//+
Line(13) = {7, 11};
//+
Line(14) = {6, 10};
//+
Line(15) = {8, 13};
//+
Line(16) = {9, 12};
//+
Point(14) = {-5, -0.9, 0, 1.0};
//+
Point(15) = {-5, 5, 0, 1.0};
//+
Line(17) = {15, 11};
//+
Line(18) = {14, 12};
//+
Point(16) = {-5, (1 + fac) * extArcPoint, 0, 1.0};
//+
Point(17) = {-5, -(1 + fac) * extArcPoint, 0, 1.0};
//+
Line(19) = {15, 16};
//+
Line(20) = {14, 17};
//+
Line(21) = {9, 17};
//+
Line(22) = {7, 16};
//+
Line(23) = {16, 17};
//+
Line(24) = {12, 13};
//+
Line(25) = {11, 10};
//+
Point(18) = {20, 5, 0, 1.0};
//+
Point(19) = {20, -0.9, 0, 1.0};
//+
Point(20) = {20, (1 + fac) * extArcPoint, 0, 1.0};
//+
Point(21) = {20, -(1 + fac) * extArcPoint, 0, 1.0};
//+
Line(26) = {6, 20};
//+
Line(27) = {8, 21};
//+
Line(28) = {13, 19};
//+
Line(29) = {19, 21};
//+
Line(30) = {21, 20};
//+
Line(31) = {10, 18};
//+
Line(32) = {18, 20};
//+
Transfinite Curve {1, 4, 3, 2, 8, 7, 6, 5, 25, 24, 23, 30} = ncyl/4 Using Progression 1;
//+
Transfinite Curve {10, 11, 12, 9} = nr Using Progression rr;
//+
Transfinite Curve {19, 13, 14, 32, 20, 16, 15, 29, 17, 18, 22, 21} = (ninlet - ncyl/4) Using Progression 1;
//+
Transfinite Curve {26, 31, 27, 28} = nwake Using Progression rwake;
//+
Curve Loop(1) = {19, -22, 13, -17};
//+
Plane Surface(1) = {1};
//+
Curve Loop(2) = {13, 25, -14, -8};
//+
Plane Surface(2) = {2};
//+
Curve Loop(3) = {14, 31, 32, -26};
//+
Plane Surface(3) = {3};
//+
Curve Loop(4) = {26, -30, -27, -5};
//+
Plane Surface(4) = {4};
//+
Curve Loop(5) = {27, -29, -28, -15};
//+
Plane Surface(5) = {5};
//+
Curve Loop(6) = {6, 16, 24, -15};
//+
Plane Surface(6) = {6};
//+
Curve Loop(7) = {16, -18, 20, -21};
//+
Plane Surface(7) = {7};
//+
Curve Loop(8) = {7, 22, 23, -21};
//+
Plane Surface(8) = {8};
//+
Curve Loop(9) = {4, 9, -7, -12};
//+
Plane Surface(9) = {9};
//+
Curve Loop(10) = {1, 10, -8, -9};
//+
Plane Surface(10) = {10};
//+
Curve Loop(11) = {2, 11, -5, -10};
//+
Plane Surface(11) = {11};
//+
Curve Loop(12) = {3, 12, -6, -11};
//+
Plane Surface(12) = {12};
//+
Curve Loop(13) = {3, 4, 1, 2};
//+
Transfinite Surface {1};
//+
Transfinite Surface {2};
//+
Transfinite Surface {3};
//+
Transfinite Surface {4};
//+
Transfinite Surface {5};
//+
Transfinite Surface {6};
//+
Transfinite Surface {7};
//+
Transfinite Surface {8};
//+
Transfinite Surface {9};
//+
Transfinite Surface {10};
//+
Transfinite Surface {11};
//+
Transfinite Surface {12};
//+
Recombine Surface {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12};
//+
Extrude {0, 0, 1} {
  Surface{1}; Surface{2}; Surface{3}; Surface{4}; Surface{5}; Surface{6}; Surface{7}; Surface{8}; Surface{9}; Surface{10}; Surface{11}; Surface{12}; Layers {1}; Recombine;
}
//+
Physical Surface("Wall", 90) = {38, 36, 31};
//+
Physical Surface("Cylinder", 88) = {55, 52, 49, 45};
//+
Physical Surface("Side", 89) = {17, 1, 21, 2, 44, 8, 41, 48, 56, 51, 54, 11, 10, 9, 12, 25, 3, 29, 4, 6, 7, 37, 5, 33};
//+
Physical Surface("Inlet", 86) = {43, 39, 13, 16, 18, 22};
//+
Physical Surface("Outlet", 87) = {23, 26, 30};
