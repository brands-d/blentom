from bpy.props import StringProperty
from bpy.types import Operator
from bpy_extras.io_utils import ImportHelper

from ..object.atom import Atoms


class XYZImport(Operator, ImportHelper):
    """
    Operator class for importing .xyz files.
    """

    bl_idname = "import.xyz"
    bl_label = "Import .xyz"

    filename_ext = ".xyz"

    filter_glob: StringProperty(default="*.xyz", options={"HIDDEN"}, maxlen=255)

    def execute(self, context):
        """
        Executes the import operation for .xyz files.
        Reads the file using the Atoms class.
        Returns a dictionary indicating the operation is finished.
        """
        Atoms.read(self.filepath)
        return {"FINISHED"}


def menu_func_import_xyz(self, *args, **kwar):
    """
    Menu function for importing .xyz files.
    Adds the XYZImport operator to the import menu.
    """
    self.layout.operator(XYZImport.bl_idname, text="XYZ (.xyz)")
