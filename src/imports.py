from bpy.props import StringProperty
from bpy.types import Operator
from bpy_extras.io_utils import ImportHelper

from .atom import Atoms
from .wavefunction import Wavefunction


class CubeImport(Operator, ImportHelper):
    bl_idname = "import.cube"
    bl_label = "Import .cube"

    filename_ext = ".cube"

    filter_glob: StringProperty(default="*.cube", options={"HIDDEN"}, maxlen=255)

    def execute(self, context):
        Atoms.read(self.filepath)
        Wavefunction.read(self.filepath)
        return {"FINISHED"}


def menu_func_import_cube(self, *args, **kwargs):
    self.layout.operator(CubeImport.bl_idname, text="Gaussian Cube (.cube)")


class XYZImport(Operator, ImportHelper):
    bl_idname = "import.xyz"
    bl_label = "Import .xyz"

    filename_ext = ".xyz"

    filter_glob: StringProperty(default="*.xyz", options={"HIDDEN"}, maxlen=255)

    def execute(self, context):
        Atoms.read(self.filepath)
        return {"FINISHED"}


def menu_func_import_xyz(self, *args, **kwar):
    self.layout.operator(XYZImport.bl_idname, text="XYZ (.xyz)")


class POSCARImport(Operator, ImportHelper):
    bl_idname = "import.poscar"
    bl_label = "Import POSCAR"

    def execute(self, context):
        Atoms.read(self.filepath)
        return {"FINISHED"}


def menu_func_import_poscar(self, *args, **kwar):
    self.layout.operator(POSCARImport.bl_idname, text="POSCAR (POSCAR)")
