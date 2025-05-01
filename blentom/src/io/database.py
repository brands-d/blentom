from os import unlink
from urllib import request
from tempfile import NamedTemporaryFile

import bpy
from bpy.types import Operator
from bpy.props import StringProperty, BoolProperty, FloatProperty

from ..object.atom import Atoms
from ..object.isosurface import Wavefunction


class DatabaseImport(Operator):
    bl_label = "Download .cube from physikmdb.uni-graz.at"
    bl_idname = "wm.databaseimport"

    url: StringProperty(name="Enter URL", default="physikmdb.uni-graz.at/cubefiles/...")
    load_atoms: BoolProperty(
        name="Atoms",
        description="Load the atomic structure",
        default=True,
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

    def draw(self, context):
        layout = self.layout

        layout.prop(self, "url")
        layout.use_property_split = True

        # Atoms
        layout.label(text="Atoms")
        box = self.layout.box()
        box.prop(self, "load_atoms", text="Load", toggle=False)

        # Density
        layout.label(text="Density")
        box = self.layout.box()
        box.prop(self, "load_density", text="Load", toggle=False)
        box.prop(self, "scale")

    def execute(self, context):
        if hasattr(bpy.app, "online_access") and not bpy.app.online_access:
            self.report(
                {"ERROR"},
                "Internet access not allowed. Change under 'Preferences -> System -> Network -> Allow Online Access'.",
            )
        else:
            try:
                with request.urlopen(self.url) as response:
                    content = response.read().decode("utf-8")

                mock_file = NamedTemporaryFile(mode="w", suffix=".cube", delete=False)
                mock_file.write(content)
                name_start = content.find("\n") + 2
                name_end = content.find("\n", name_start)

            except Exception:
                return {"CANCELLED"}

        if self.load_atoms:
            Atoms.read(mock_file.name, name=content[name_start:name_end], format="cube")

        if self.load_density:
            scale = self.scale if float(self.scale) != 1.0 else None
            Wavefunction.read(
                mock_file.name,
                name=content[name_start:name_end],
                format=".cube",
                scale=scale,
            )

        mock_file.close()
        unlink(mock_file.name)
        return {"FINISHED"}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)


def menu_func_import_database(self, *args, **kwargs):
    """
    Menu function for importing .cube files from the database.
    """
    self.layout.operator(
        DatabaseImport.bl_idname, text="physikmdb.uni-graz.at  (.cube)"
    )
