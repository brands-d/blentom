import bpy  # type: ignore
from math import degrees  # type: ignore
from mathutils import Vector, Euler  # type: ignore

from .base import BlenderObject


class Plane(BlenderObject):
    def __init__(
        self, size=(100, 100), location=(0, 0, -10), rotation=(0, 0, 0), material=None
    ):
        bpy.ops.mesh.primitive_plane_add(location=location)
        self.blender_object = bpy.context.active_object
        self.size = size
        if material is not None:
            self.material = material
        super().__init__()

    @property
    def orientation(self):
        return (
            Euler(self.rotation, "XYZ").to_matrix() @ Vector((0, 0, 1))
        ).normalized()

    @orientation.setter
    def orientation(self, orientation):
        self.rotation = [
            degrees(angle)
            for angle in Vector(orientation).to_track_quat("Z", "Y").to_euler()
        ]

    @property
    def size(self):
        return list(self.blender_object.scale[:2])

    @size.setter
    def size(self, size):
        self.blender_object.scale = (size[0], size[1], 1)
