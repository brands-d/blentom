from bpy.types import Operator
from bpy_extras.io_utils import ImportHelper

from ..object.atom import Atoms


class POSCARImport(Operator, ImportHelper):
    """
    Operator class for importing POSCAR files.
    """

    bl_idname = "import.poscar"
    bl_label = "Import POSCAR"

    def execute(self, context):
        """
        Executes the import operation for POSCAR files.
        Reads the file using the Atoms class.
        Returns a dictionary indicating the operation is finished.
        """
        Atoms.read(self.filepath)
        return {"FINISHED"}


def menu_func_import_poscar(self, *args, **kwar):
    """
    Menu function for importing POSCAR files.
    Adds the POSCARImport operator to the import menu.
    """
    self.layout.operator(POSCARImport.bl_idname, text="POSCAR (POSCAR)")
