import bpy
from mathutils import Vector
from numpy import diag, ndarray

from .bond import Bond
from .collection import Collection
from .meshobject import MeshObject
from .object import Object


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


class Atoms(MeshObject):
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

        if repetitions == (0, 0, 0):
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
