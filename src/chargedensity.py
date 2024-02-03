from pathlib import Path

import bpy
from ase.calculators.vasp import VaspChargeDensity
from mathutils import Vector
from numpy import diag, ndarray, tile

from .lib import flip_normals, marching_cubes
from .meshobject import MeshObject


class ChargeDensity(MeshObject):
    def __init__(
        self,
        density,
        unit_cell=((1, 0, 0), (0, 1, 0), (0, 0, 1)),
        name="Charge Density",
        level=None,
        filename=None,
    ):
        object = marching_cubes(density, unit_cell, name, level)
        bpy.data.collections["Collection"].objects.link(object)
        flip_normals(object)
        super().__init__()

        self._unit_cell = unit_cell
        self.density = density
        self._level = level

    @classmethod
    def read(cls, filename, name=None, level=None):
        if name is None:
            name = Path(filename).stem
        density = VaspChargeDensity(filename).chg[-1]
        unit_cell = VaspChargeDensity(filename).atoms[-1].cell
        return ChargeDensity(density, unit_cell, name, level=level)

    @property
    def level(self):
        return self._level

    @level.setter
    def level(self, level):
        density = self.density
        unit_cell = self.unit_cell
        name = self.name

        bpy.data.collections["Collection"].objects.unlink(self.blender_object)
        bpy.data.objects.remove(self.blender_object, do_unlink=True)
        new = ChargeDensity(density, unit_cell, name, level)
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
