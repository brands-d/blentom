from pathlib import Path

import bpy
from ase.calculators.vasp import VaspChargeDensity
from mathutils import Vector
from numpy import diag, ndarray, tile

from .lib import flip_normals, marching_cubes, read_cube
from .meshobject import MeshObject


class ChargeDensity(MeshObject):
    def __init__(
        self,
        density,
        unit_cell=((1, 0, 0), (0, 1, 0), (0, 0, 1)),
        origin=(0, 0, 0),
        name="Charge Density",
        level=None,
    ):
        object = marching_cubes(density, unit_cell, name, level)
        bpy.data.collections["Collection"].objects.link(object)
        flip_normals(object)
        super().__init__()

        self._origin = origin
        self._unit_cell = unit_cell
        self.density = density
        self._level = level

    @classmethod
    def read(cls, filename, name=None, level=None, format=None):
        filename = Path(filename)
        if name is None:
            name = filename.stem

        if format is None:
            format = filename.suffix if filename.suffix else filename.stem

        if format == ".cube":
            density, origin, axes, unit_cell = read_cube(filename)
            unit_cell = axes
        elif format.lower() in ("parchg", "chgcar"):
            density = VaspChargeDensity(filename).chg[-1]
            unit_cell = VaspChargeDensity(filename).atoms[-1].cell
            origin = (0, 0, 0)
        else:
            raise ValueError(f"Unsupported file format: {format}")

        return ChargeDensity(density, unit_cell, origin, name, level=level)

    @classmethod
    def from_cube(cls, filename, name=None, level=None):
        return cls.read(filename, name, level, format=".cube")

    @property
    def level(self):
        return self._level

    @level.setter
    def level(self, level):
        density = self.density
        unit_cell = self.unit_cell
        origin = self._origin
        name = self.name

        bpy.data.collections["Collection"].objects.unlink(self.blender_object)
        bpy.data.objects.remove(self.blender_object, do_unlink=True)
        new = ChargeDensity(density, unit_cell, origin, name, level)
        self.blender_object = new.blender_object

    @property
    def unit_cell(self):
        return self._unit_cell

    @unit_cell.setter
    def unit_cell(self, unit_cell):
        if isinstance(unit_cell[0], (ndarray, tuple, Vector, list)):
            self._unit_cell = unit_cell
        else:
            self._unit_cell = diag(unit_cell)

    def repeat(self, repetitions):
        if repetitions == (0, 0, 0):
            return

        repetitions = tuple([repetition + 1 for repetition in repetitions])
        self.density = tile(self.density, repetitions)
        self.unit_cell = diag(repetitions) @ self.unit_cell
        self.level = self.level
