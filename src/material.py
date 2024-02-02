from pathlib import Path

import bpy

from .periodic_table import PeriodicTable


class Material:
    material_directory = Path(Path(__file__).parent / "resources" / "materials.blend")

    def __init__(self, name):
        if len(name) <= 2:
            try:
                name = PeriodicTable[name].name
            except KeyError:
                name = "Unknown"

        self._material = bpy.data.materials.get(name)
        if self._material is None:
            try:
                bpy.ops.wm.append(
                    filepath="/Material/" + name,
                    filename=name,
                    directory=str(Material.material_directory) + "/Material/",
                )
            except RuntimeError:
                print("Current file needs to have been saved at least once.")
                return None
            else:
                self._material = bpy.data.materials.get(name)

    @property
    def material(self):
        return self._material

    @material.setter
    def material(self, material):
        self._material = material
