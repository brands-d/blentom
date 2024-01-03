from numpy import mat
import bpy  # type: ignore
from math import radians  # type: ignore
from mathutils import Matrix, Vector, Euler  # type: ignore


class BlenderObject:
    @property
    def position(self):
        return list(self.blender_object.location)

    @position.setter
    def position(self, position):
        self.blender_object.location = Vector(position)

    @property
    def rotation(self):
        return list(self.blender_object.rotation_euler)

    @rotation.setter
    def rotation(self, rotation):
        self.blender_object.rotation_euler = Euler(
            [radians(angle) for angle in rotation], "XYZ"
        )
        bpy.ops.object.transform_apply()

    @property
    def material(self):
        return self.blender_object.active_material

    @material.setter
    def material(self, material):
        self.blender_object.active_material = material.material

    def move(self, translation):
        self.position = self.blender_object.location + Vector(translation)

    def rotate(self, degrees, axis="Z", center="local"):
        original = self.blender_object.matrix_world
        if isinstance(axis, str):
            rotation = Matrix.Rotation(radians(degrees), 4, axis.upper())
        else:
            rotation = Matrix.Rotation(radians(degrees), 4, Vector(axis).normalized())
        if isinstance(center, str):
            if center.lower() == "local":
                center = Vector((0, 0, 0))
            elif center.lower() == "origin":
                center = original.decompose()[0]
        shift = Matrix.Translation(center)

        self.blender_object.matrix_world = (
            shift @ rotation @ shift.inverted() @ original
        )
        bpy.ops.object.transform_apply()

    def periodic(self, periodicity=False, cell=None):
        if cell is None:
            try:
                cell = self.cell
            except AttributeError:
                cell = ((1, 0, 0), (0, 1, 0), (0, 0, 1))

        if not periodicity:
            pass
        else:
            for i, (periodic, label) in enumerate(zip(periodicity, "XYZ")):
                if periodic <= 1:
                    pass
                else:
                    self.blender_object.modifiers.new(f"Periodicity {label}", "ARRAY")
                    modifier = self.blender_object.modifiers[f"Periodicity {label}"]
                    modifier.use_relative_offset = False
                    modifier.use_constant_offset = True
                    if i != 0:
                        modifier.constant_offset_displace[0] = 0
                    modifier.count = periodic
                    modifier.constant_offset_displace = cell[i]

    def delete(self):
        bpy.data.objects.remove(self.blender_object, do_unlink=True)


def reset():
    bpy.ops.object.select_all(action="DESELECT")
    bpy.ops.object.select_by_type(type="MESH")
    bpy.ops.object.delete()
    bpy.ops.object.select_by_type(type="LIGHT")
    bpy.ops.object.delete()
