import FreeCAD
from FreeCAD import Base, Vector, Gui
import Part
import ObjectsFem
#print(dir(Part))
from math import pi, sin, cos
#import objectsFEM
#print(dir(FreeCAD))
#import  importToolsFem
DOC = FreeCAD.activeDocument()
#for  obj in DOC.Objects:
	#print(obj.Name)
	#obj_b = DOC.addObject("Part::Box")
	#print(obj.Name)
#	pass
add_obj=DOC.addObject("Part::Box", "Box")
#print([i.Name for i in DOC.Objects])
add_obj.Length =	80 #mm
add_obj.Width =	1000 #mm
add_obj.Height =	10 #mm

analysis_ = ObjectsFem.makeAnalysis(DOC,"analysis")
solving= ObjectsFem.makeSolverCalculixCcxTools(DOC,"Calculix")
#print(dir(solving))
solving.GeometricalNonlinearity= "linear"
solving.ThermoMechSteadyState = True
solving.MatrixSolverType="default" #unknown
solving.IterationsControlParameterTimeUse = False #unknown
analysis_.addObject(solving)


material_=ObjectsFem.makeMaterialSolid(DOC, "SolidMaterial")
matt=material_.Material
matt["YoungsModulus"]="21000 MPa"
matt["PoissonRatio"]="0.30"
matt["Density"] = "7900 kg/m^3"
material_.Material=matt
analysis_.addObject(material_)

#fixed constraints
fixed_c=ObjectsFem.makeConstraintFixed(DOC,"FemConstraintFixed")

fixed_c.References=[(DOC.Box), "Face1"]
analysis_.addObject(fixed_c)

#force constraint
force_c=ObjectsFem.makeConstraintForce(DOC,"FemConstraintForce")
force_c.References=[(DOC.Box, "Face2")]
force_c.Force=900000.0
force_c.Direction=(DOC.Box,["Edge5"] )
force_c.Reversed=True
analysis_.addObject(force_c)


#FEM mesh gmsh

#fem_mesh=ObjectsFem.makeMeshGmsh(DOC,"Mesh1")
#fem_mesh.Part=DOC.Box
#DOC.recompute()


#from femmesh.gmshtools import GmshTools as gt
#gmsh_mesh=gt(fem_mesh)
#error=gmsh_mesh.create_mesh()
#print(error)

#analysis_.addObject(fem_mesh)

mesh=DOC.addObject("Fem::FemMeshShapeNetgenObject", "FEMMeshNetgen")
mesh.Shape=DOC.Box
mesh.MaxSize=1000 #mm
mesh.Fineness= "Moderate"
mesh.Optimize= True
mesh.SecondOrder = True
#print([i for i in mesh])
DOC.recompute()
analysis_.addObject(mesh)
#print([i for i in analysis_.addObject(mesh)])
DOC.recompute()


#activated
import FemGui
FemGui.setActiveAnalysis(DOC.analysis)
#running
#from femtools import ccxtools
#fea = ccxtools.FemToolsCcx()
#fea.purge_results()
#fea.run()


from femtools import ccxtools
fea = ccxtools.FemToolsCcx()
fea.update_objects()
fea.setup_working_dir()
fea.setup_ccx()
message = fea.check_prerequisites()

fea.purge_results()
fea.write_inp_file()
    # on error at inp file writing, the inp file path "" was returned (even if the file was written)
    # if we would write the inp file anyway, we need to again set it manually
#fea.inp_file_name = '/tmp/FEMWB/FEMMeshGmsh.inp'
fea.ccx_run()
fea.load_results()