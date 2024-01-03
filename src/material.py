from pathlib import Path
import bpy  # type: ignore

from json import load


class Material:
    def __init__(self, name="New Material", properties={}):
        self.material = bpy.data.materials.new(name=name)
        self.material.use_nodes = True
        self.material.use_backface_culling = True
        self.material.blend_method = "BLEND"
        self.node = self.material.node_tree.nodes["Principled BSDF"]
        self.properties = properties

    @classmethod
    def pre_defined(cls, name):
        with open(Path(__file__).parent / "resources" / "materials.json") as file:
            data = load(file)

        for material in data:
            if material["Name"] == name:
                return Material(name, material["Properties"])
        return None

    @property
    def base_color(self):
        return self.node.inputs["Base Color"].default_value[:]

    @base_color.setter
    def base_color(self, color):
        self.node.inputs["Base Color"].default_value = color

    @property
    def properties(self):
        properties = {"Base Color": self.base_color, "Settings": self.settings}
        return properties

    @properties.setter
    def properties(self, properties):
        for key, value in properties.items():
            try:
                self.node.inputs[key].default_value = value
            except AttributeError:
                pass
