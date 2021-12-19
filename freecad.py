"""freecad.py

   Primo script per FreeCAD

"""

import FreeCAD
from FreeCAD import Base, Vector
import Part
from math import pi, sin, cos


DOC = FreeCAD.activeDocument()
for  obj in DOC.Objects:
	#print(obj.Name)
	#obj_b = DOC.addObject("Part::Box")
	#print(obj.Name)
	pass
add_obj=DOC.addObject("Part::Box")
print([i.Name for i in DOC.Objects])
add_obj.Length =	10 #mm
add_obj.Width =	10 #mm
add_obj.Height =	10 #mm