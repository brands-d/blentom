from bpy.types import Operator
from bpy_extras.io_utils import ImportHelper

from ..object.atom import Atoms
from ..object.isosurface import ChargeDensity


class CHGCARImport(Operator, ImportHelper):
    """
    Operator class for importing CHGCAR files.
    """

    bl_idname = "import.chgcar"
    bl_label = "Import CHGCAR"

    def execute(self, context):
        """
        Executes the import operation for CHGCAR files.
        Reads the file using the Atoms and ChargeDensity classes.
        Returns a dictionary indicating the operation is finished.
        """
        Atoms.read(self.filepath)
        ChargeDensity.read(self.filepath)
        return {"FINISHED"}


def menu_func_import_chgcar(self, *args, **kwargs):
    """
    Menu function for importing CHGCAR files.
    Adds the CHGCARImport operator to the import menu.
    """
    self.layout.operator(CHGCARImport.bl_idname, text="CHGCAR/PARCHG")
