import bpy  # type: ignore
from mathutils import Vector  # type: ignore
from math import acos, atan2, degrees  # type: ignore

from .material import Material
from .base import BlenderObject


class Bond(BlenderObject):
    def __init__(self, atom_1, atom_2, **kwargs):
        self.cell = atom_1.cell
        distance = Vector(atom_1.position) - Vector(atom_2.position)
        location = Vector(atom_1.position) - distance / 2
        bpy.ops.mesh.primitive_cylinder_add(radius=0.10, vertices=25, location=location)
        self.blender_object = bpy.context.object
        self.blender_object.scale[2] = distance.length / 2
        self.rotation = (
            0,
            degrees(acos(distance[2] / distance.length)),
            degrees(atan2(distance[1], distance[0])),
        )
        self.blender_object.data.polygons.foreach_set(
            "use_smooth", [True] * len(self.blender_object.data.polygons)
        )
        self.material = Material.pre_defined("Bond")
        super().__init__(**kwargs)
