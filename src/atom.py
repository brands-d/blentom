from pathlib import Path
from itertools import product, combinations

import bpy
from ase.io import read
from mathutils import Vector
from numpy import diag, ndarray

from .bond import Bond
from .collection import Collection
from .meshobject import MeshObject
from .object import Object


class Atom(MeshObject):

    _atoms = []

    def __init__(self, element="X"):
        # TODO
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.5)
        super().__init__()

        self.element = element
        self.name = element

        Atom._atoms.append(self)

    @classmethod
    def ase(cls, atom):
        self = Atom(atom.symbol)
        self.location = atom.position
        return self

    @classmethod
    def get(cls, filter=None):
        Atom._clean()

        if filter is None or filter == "all":
            return cls._atoms
        elif isinstance(filter, str) and len(filter) <= 2:
            return [atom for atom in cls._atoms if atom.element == filter]
        elif callable(filter):
            return [atom for atom in cls._atoms if filter(atom)]

    @classmethod
    def _clean(cls):
        for atom in cls._atoms:
            if atom.blender_object is None:
                cls._atoms.remove(atom)

    def __add__(self, other):
        if isinstance(other, Atom):
            atoms = Atoms("New Atoms")
            atoms += self
            atoms += other
            return atoms
        elif isinstance(other, Atoms):
            other += self
            return other

    def delete(self):
        self._atoms.remove(self)
        super().delete()


class Atoms(MeshObject):
    def __init__(self, name):
        self._atoms = []
        self._unit_cell = None
        self.copies = []

        self.collection = Collection(name)
        self.atoms_collection = Collection("Atoms")
        self.collection.link(self.atoms_collection)
        self.bonds_collection = Collection("Bonds")
        self.collection.link(self.bonds_collection)

    @classmethod
    def ase(cls, atoms, name):
        self = Atoms(name)
        self.unit_cell = atoms.cell[:]
        for atom in atoms:
            self += Atom.ase(atom)

        return self

    @classmethod
    def read(cls, filename, name=None):
        filename = Path(filename)
        if name is None:
            name = filename.stem

        return Atoms.ase(read(str(filename)), name=name)

    def __add__(self, objects):
        if not isinstance(objects, (list, tuple)):
            objects = (objects,)
        for object in objects:
            if isinstance(object, Atom):
                _ = self.atoms_collection + object
                self._atoms.append(object)
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

    def get(self, filter=None):
        self.clean()

        if filter is None or filter == "all":
            return self._atoms
        elif isinstance(filter, str) and len(filter) <= 2:
            return [atom for atom in self._atoms if atom.element == filter]
        elif callable(filter):
            return [atom for atom in self._atoms if filter(atom)]

    def clean(self):
        for atom in self._atoms:
            if atom.blender_object is None:
                self._atoms.remove(atom)

    def create_bonds(self, periodic=False):
        for atom_1, atom_2 in combinations(self.get("all"), 2):
            for x, y, z in (p for p in product((-1, 0, 1), repeat=3)):
                shift = Vector(
                    x * self.unit_cell[0]
                    + y * self.unit_cell[1]
                    + z * self.unit_cell[2]
                )
                if (
                    Vector(atom_1.position) - Vector(atom_2.position) - Vector(shift)
                ).length <= 1.5:
                    if (x, y, z) != (0, 0, 0) and periodic:
                        atom_2 = _DummyAtom(atom_2)
                        atom_2.position = Vector(atom_2.position) + shift

                    self += Bond(atom_1, atom_2)

    def repeat(self, repetitions):
        if repetitions == (0, 0, 0):
            return
        else:
            if self.unit_cell is None:
                raise RuntimeError("No unit cell defined.")

            self.copies_collection = Collection(f"{self.name} Copies")
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


class _DummyAtom:
    def __init__(self, atom):
        self.position = atom.position
        self.name = atom.name
