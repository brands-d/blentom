from pathlib import Path
from json import load

import bpy

from .periodic_table import PeriodicTable


class Material:
    material_directory = Path(Path(__file__).parent / "resources" / "materials.blend")
    fallback_file = Path(Path(__file__).parent / "resources" / "materials.json")

    def __init__(self, name):
        if len(name) <= 2:
            try:
                name = PeriodicTable[name].name
            except KeyError:
                name = "Unknown"

        material = bpy.data.materials.get(name)
        if material is None:
            try:
                Material.load_preset_material(name)
            except KeyError:
                print("Material not found in presets.")

        material = bpy.data.materials.get(name)
        if material is None:
            try:
                Material.load_fallback_material(name)
            except KeyError:
                print("Material not found in fallback catalog.")

        material = bpy.data.materials.get(name)
        if material is None:
            material = Material.create(name)

        self._material = material

    @property
    def material(self):
        return self._material

    @material.setter
    def material(self, material):
        self._material = material

    @classmethod
    def load_fallback_material(cls, name):
        with open(Material.fallback_file) as file:
            data = load(file)

        for material in data:
            if material["name"] == name:
                Material.create(name, material["properties"])
                break

    @classmethod
    def load_preset_material(cls, name):
        bpy.ops.wm.append(
            filepath="/Material/" + name,
            filename=name,
            directory=str(Material.material_directory) + "/Material/",
        )
        material = bpy.data.materials.get(name)

        if material is None:
            raise KeyError(f"Material {name} not found")
        else:
            return material

    @classmethod
    def create(cls, name, properties={}):
        material = bpy.data.materials.new(name=name)
        material.use_nodes = True
        material.use_backface_culling = True
        material.blend_method = "BLEND"
        node = material.node_tree.nodes["Principled BSDF"]

        for key, value in properties.items():
            try:
                node.inputs[key].default_value = value
            except KeyError:
                pass
