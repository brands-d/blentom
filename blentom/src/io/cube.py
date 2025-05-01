from bpy.props import StringProperty, BoolProperty, FloatProperty
from bpy.types import Operator
from bpy_extras.io_utils import ImportHelper

from ..object.atom import Atoms
from ..object.isosurface import Wavefunction


class CubeImport(Operator, ImportHelper):
    """
    Import a Gaussian .cube file.
    """

    bl_idname = "import.cube"
    bl_label = "Import .cube"

    filename_ext = ".cube"

    filter_glob: StringProperty(default="*.cube", options={"HIDDEN"}, maxlen=6)
    load_atoms: BoolProperty(
        name="Atoms",
        description="Load the atomic structure",
        default=True,
    )
    show_double_bonds: BoolProperty(
        name="Double & Triple Bonds",
        description="Add double and triple bonds.",
        default=False,
    )
    load_density: BoolProperty(
        name="Density",
        description="Load the 3D scalar density as isosurface",
        default=True,
    )
    scale: FloatProperty(
        name="Interpolation",
        description="Interpolates density onto finer grid before creating isosurface mesh. Yields better mesh results at cost of loading times. Rendering performance not changed due to remesh modifier. Set to 1 to disable.",
        precision=1,
        min=1,
        max=5,
        soft_max=2,
        step=0.5,
        default=2,
    )

    def execute(self, _):
        """
        Executes the import operation for .cube files.
        Reads the file using the Atoms and Wavefunction classes.
        Returns a dictionary indicating the operation is finished.
        """
        if self.load_atoms:
            Atoms.read(self.filepath, double_bonds=self.show_double_bonds)

        if self.load_density:
            if self.scale != 1:
                Wavefunction.read(self.filepath, scale=self.scale)
            else:
                Wavefunction.read(self.filepath)

        return {"FINISHED"}

    def draw(self, context):
        layout = self.layout

        # Atoms
        layout.label(text="Atoms")
        box = self.layout.box()
        box.prop(self, "load_atoms", text="Load", toggle=False)
        box.prop(self, "show_double_bonds", text="Double & Triple Bonds", toggle=False)

        # Density
        layout.label(text="Density")
        box = self.layout.box()
        box.prop(self, "load_density", text="Load", toggle=False)
        box.prop(self, "scale")


def menu_func_import_cube(self, *args, **kwargs):
    """
    Menu function for importing .cube files.
    Adds the CubeImport operator to the import menu.
    """
    self.layout.operator(CubeImport.bl_idname, text="Gaussian Cube (.cube)")
