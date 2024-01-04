from ase import Atom
from bpy_extras.io_utils import ImportHelper
from bpy.props import StringProperty
from bpy.types import Operator

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


class XYZImport(Operator, ImportHelper):
    bl_idname = "import.xyz"
    bl_label = "Import .xyz"

    filename_ext = ".xyz"

    filter_glob: StringProperty(default="*.xyz", options={"HIDDEN"}, maxlen=255)

    def execute(self, context):
        Atoms.read(self.filepath)
        return {"FINISHED"}


class POSCARImport(Operator, ImportHelper):
    bl_idname = "import.poscar"
    bl_label = "Import POSCAR"

    def execute(self, context):
        Atoms.read(self.filepath)
        return {"FINISHED"}
