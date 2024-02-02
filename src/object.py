from mathutils import Vector, Euler
from math import radians, degrees, acos, atan2
import bpy
from copy import copy
from numpy import diag, ndarray


class Object:
    def __init__(self, object=None):
        self._blender_object = object

    @property
    def blender_object(self):
        try:
            self._blender_object.name
        except ReferenceError:
            return None
        except AttributeError:
            return None
        else:
            return self._blender_object

    @blender_object.setter
    def blender_object(self, blender_object):
        self._blender_object = blender_object

    @property
    def location(self):
        return list(self.blender_object.location)

    @location.setter
    def location(self, location):
        self.blender_object.location = Vector(location)

    @property
    def position(self):
        return self.location

    @position.setter
    def position(self, position):
        self.location = Vector(position)

    @property
    def rotation(self):
        return [degrees(angle) for angle in self.blender_object.rotation_euler]

    @rotation.setter
    def rotation(self, rotation):
        self.blender_object.rotation_euler = Euler(
            [radians(angle) for angle in rotation], "XYZ"
        )

    @property
    def name(self):
        return self.blender_object.name

    @name.setter
    def name(self, name):
        self.blender_object.name = name
        for object in bpy.data.objects.values():
            if object.data is not None:
                object.data.name = name

    def make_active(self):
        bpy.ops.object.select_all(action="DESELECT")
        self.blender_object.select_set(True)
        bpy.context.view_layer.objects.active = self.blender_object

    def move(self, translation):
        self.location = Vector(self.blender_object.location) + Vector(translation)

    def rotate(self, rotation, origin="local"):
        if origin == "local":
            bpy.ops.object.origin_set(type="ORIGIN_GEOMETRY")
            self.rotation = Vector(rotation) + Vector(self.rotation)
        elif origin in ("global", "cursor"):
            bpy.ops.object.origin_set(type="ORIGIN_CURSOR")
            self.rotation = Vector(rotation) + Vector(self.rotation)
            bpy.ops.object.origin_set(type="ORIGIN_GEOMETRY")
        else:
            previous_cursor_location = bpy.context.scene.cursor.location.copy()

            if origin in ("world", "origin"):
                bpy.context.scene.cursor.location = Vector((0, 0, 0))
            elif isinstance(origin, (tuple, list, Vector)):
                bpy.context.scene.cursor.location = Vector(origin)
            elif isinstance(origin, (Object, bpy.types.Object)):
                bpy.context.scene.cursor.location = Vector(origin.location)

            self.make_active()
            bpy.ops.object.origin_set(type="ORIGIN_CURSOR")
            self.rotation = Vector(rotation) + Vector(self.rotation)
            bpy.ops.object.origin_set(type="ORIGIN_GEOMETRY")
            bpy.context.scene.cursor.location = previous_cursor_location

    def delete(self):
        if self.blender_object is not None:
            bpy.data.objects.remove(self.blender_object, do_unlink=True)
            self._blender_object = None

    def __del__(self):
        self.delete()


class MeshObject(Object):
    def __init__(self):
        super().__init__()
        self.blender_object = bpy.context.active_object

    @property
    def scale(self):
        return list(self.blender_object.scale)

    @scale.setter
    def scale(self, scale):
        self.blender_object.scale = Vector(scale)


class Atom(MeshObject):
    def __init__(self, element="X"):
        bpy.ops.mesh.primitive_uv_sphere_add()
        super().__init__()

        self.element = element
        self.name = element

    def __add__(self, other):
        if isinstance(other, Atom):
            atoms = Atoms("New Atoms")
            atoms += self
            atoms += other
            return atoms
        elif isinstance(other, Atoms):
            other += self
            return other


class Bond(MeshObject):
    def __init__(self, atom_1, atom_2):
        self.atom_1 = atom_1
        self.atom_2 = atom_2
        distance = Vector(atom_1.position) - Vector(atom_2.position)
        location = Vector(atom_1.position) - distance / 2

        bpy.ops.mesh.primitive_cylinder_add(location=location)
        super().__init__()

        self.position = location
        self.rotation = (
            0,
            degrees(acos(distance[2] / distance.length)),
            degrees(atan2(distance[1], distance[0])),
        )
        self.scale = (0.1, 0.1, distance.length / 2)

        self.name = f"{atom_1.name}-{atom_2.name}"


class Collection:
    def __init__(self, name="New Collection"):
        if name in bpy.data.collections:
            self.collection = bpy.data.collections[name]
        else:
            self.collection = bpy.data.collections.new(name)
            bpy.context.scene.collection.children.link(self.collection)

    @property
    def name(self):
        return self.collection.name

    @name.setter
    def name(self, name):
        self.collection.name = name

    def __add__(self, objects):
        if not isinstance(objects, (list, tuple)):
            objects = (objects,)
        for object in objects:
            self.collection.objects.link(object.blender_object)
            self._unlink_from_scene_collections(object.blender_object)

        return self

    def link(self, collection):
        try:
            self.collection.children.link(collection.collection)
            bpy.context.scene.collection.children.unlink(collection.collection)
        except RuntimeError:
            pass

    def remove_object(self, objects):
        if not isinstance(objects, (list, tuple)):
            objects = (objects,)
        for object in objects:
            self.collection.objects.unlink(object.blender_object)

    def dissolve(self):
        for object in self.collection.objects:
            bpy.context.scene.collection.objects.link(object)
            self.collection.objects.unlink(object)

        bpy.data.collections.remove(self.collection)

    def _unlink_from_scene_collections(self, object):
        for collection in bpy.context.scene.collection.children:
            if collection.name != self.collection.name:
                if object.name in collection.objects:
                    collection.objects.unlink(object)

        if object.name in bpy.context.scene.collection.objects:
            bpy.context.scene.collection.objects.unlink(object)

    def delete(self):
        for object in self.collection.objects:
            object.delete()
        bpy.data.collections.remove(self.collection)


# TODO Make Meshobject for whole collection
class Atoms:
    def __init__(self, name):
        self._unit_cell = None
        self.copies = []

        self.collection = Collection(name)
        self.atoms_collection = Collection("Atoms")
        self.collection.link(self.atoms_collection)
        self.bonds_collection = Collection("Bonds")
        self.collection.link(self.bonds_collection)

    def __add__(self, objects):
        if not isinstance(objects, (list, tuple)):
            objects = (objects,)
        for object in objects:
            if isinstance(object, Atom):
                _ = self.atoms_collection + object
            elif isinstance(object, Bond):
                _ = self.bonds_collection + object

        return self

    @property
    def name(self):
        return self.collection.name

    @name.setter
    def name(self, name):
        self.collection.name = name

    @property
    def unit_cell(self):
        return self._unit_cell

    @unit_cell.setter
    def unit_cell(self, cell):
        if isinstance(cell[0], (ndarray, tuple, Vector, list)):
            self._unit_cell = cell
        else:
            self._unit_cell = diag(cell)

    def repeat(self, repetitions):
        self.copies_collection = Collection(f"{self.name} Copies")

        if repetitions in (
            None,
            (1, 1, 1),
            [1, 1, 1],
            (0, 0, 0),
            (1, 1, 1),
            "none",
            "None",
            False,
            "no",
        ):
            return
        else:
            if self.unit_cell is None:
                raise RuntimeError("No unit cell defined.")

            repetitions = [
                range(min(0, repetition), max(0, repetition) + 1)
                for repetition in repetitions
            ]
            for x in repetitions[0]:
                for y in repetitions[1]:
                    for z in repetitions[2]:
                        if (x == 0 and y == 0 and z == 0) or (
                            x == 1 and y == 1 and z == 1
                        ):
                            continue
                        copy = self._new_instance_to_scene(
                            f"{self.name} - ({x:d}, {y:d}, {z:d})"
                        )
                        copy.location = (
                            x * Vector(self.unit_cell[0])
                            + y * Vector(self.unit_cell[1])
                            + z * Vector(self.unit_cell[2])
                        )
                        self.copies.append(copy)

    def _new_instance_to_scene(self, name):
        instance = Object()
        instance.blender_object = bpy.data.objects.new(name=name, object_data=None)
        instance.blender_object.instance_type = "COLLECTION"
        instance.blender_object.instance_collection = self.collection.collection
        self.copies_collection + instance

        return instance
