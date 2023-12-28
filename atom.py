import bpy  # type: ignore
from mathutils import Vector  # type: ignore
from ase.io import read

from itertools import combinations
from blentom.base import BlenderObject  # type: ignore
from blentom.material import Material  # type: ignore
from blentom.periodic_table import PeriodicTable  # type: ignore
from blentom.bond import Bond  # type: ignore


class Atom(BlenderObject):
    def __init__(
        self, symbol, location=(0, 0, 0), cell=((1, 0, 0), (0, 1, 0), (0, 0, 1))
    ):
        self.cell = cell
        self.symbol = symbol
        element = PeriodicTable[symbol]
        self.covalent_radius = element.covalent_radius
        radius = element.radius

        bpy.ops.mesh.primitive_uv_sphere_add(radius=radius, location=location)
        self.blender_object = bpy.context.active_object
        self.blender_object.data.polygons.foreach_set(
            "use_smooth", [True] * len(self.blender_object.data.polygons)
        )
        self.material = element.material

    @property
    def radius(self):
        return self.blender_object.scale[0]

    @radius.setter
    def radius(self, radius):
        self.blender_object.scale = (radius, radius, radius)


class Atoms:
    def __init__(self, atoms, bonds=1.2):
        self.cell = atoms.cell[:]
        self.atoms = []
        for atom in atoms:
            self.atoms.append(Atom(atom.symbol, atom.position, cell=self.cell))

        if bonds:
            self.bonds = []
            for atom_i, atom_j in combinations(self.atoms, 2):
                distance = (Vector(atom_i.position) - Vector(atom_j.position)).length
                if distance <= 1.2 * (atom_i.covalent_radius + atom_j.covalent_radius):
                    self.bonds.append(Bond(atom_i, atom_j))

    @classmethod
    def read(cls, filename):
        return Atoms(read(filename))

    @property
    def positions(self):
        return tuple([atom.position for atom in self.atoms])

    @positions.setter
    def positions(self, positions):
        if len(positions) == len(self.atoms):
            for atom, position in zip(self.atoms, positions):
                atom.position = position

    def periodic(self, periodicity=False):
        for atom in self.atoms:
            atom.periodic(periodicity, self.cell)
        for bond in self.bonds:
            bond.periodic(periodicity, self.cell)

    def add_atom(self, atom):
        self.atoms.append(atom)

    def rotate(self, *args, **kwargs):
        for atom in self.atoms:
            atom.rotate(*args, **kwargs)
