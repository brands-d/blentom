import bpy  # type: ignore

from .base import BlenderObject


class Light(BlenderObject):
    first = True

    def __init__(self, energy=10, position=(0, 0, 25), rotation=(0, 0, 0)):
        self.position = position
        self.rotation = rotation
        self.energy = energy

    def __new__(cls, *args, **kwargs):
        light = super(Light, cls).__new__(cls)
        if cls.first:
            try:
                light.blender_object = bpy.data.objects["Light"]
            except KeyError:
                bpy.ops.object.light_add(type="SUN")
                light.blender_object = bpy.context.active_object
            else:
                light.blender_object.data.type = "SUN"
            finally:
                cls.first = False
        else:
            bpy.ops.object.light_add(type="SUN")
            light.blender_object = bpy.context.active_object

        return light

    @property
    def energy(self):
        return self.blender_object.data.energy

    @energy.setter
    def energy(self, energy):
        self.blender_object.data.energy = energy
