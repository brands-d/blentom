from pathlib import Path

import bpy
from ase.calculators.vasp import VaspChargeDensity
from numpy import diag, tile

from .lib import flip_normals, marching_cubes_gaussian, marching_cubes_VASP, read_cube
from .meshobject import MeshObject


class Isosurface(MeshObject):
    def __init__(self, isosurface_object):
        self._isosurface_object = isosurface_object
        self._link()
        super().__init__()

    @classmethod
    def read(cls, filename, name=None, level=None, format=None):
        filename = Path(filename)
        if name is None:
            name = filename.stem

        if format is None:
            format = filename.suffix if filename.suffix else filename.stem

        if format == ".cube":
            return Isosurface(CubeIsosurface(filename, name, level))
        elif format.lower() in ("parchg", "chgcar"):
            return Isosurface(VaspIsosurface(filename, name, level))
        else:
            raise ValueError(f"Unsupported file format: {format}")

    @property
    def blender_object(self):
        return self._isosurface_object.blender_object

    @blender_object.setter
    def blender_object(self, blender_object):
        self._isosurface_object.blender_object = blender_object

    @property
    def level(self):
        return self._isosurface_object.level

    @level.setter
    def level(self, level):
        self._isosurface_object.level = level
        self.update()

    @property
    def name(self):
        return self._isosurface_object._name

    @name.setter
    def name(self, name):
        self._isosurface_object._name = name

    def repeat(self, repetitions):
        self._isosurface_object.repetitions = repetitions
        self.update()

    def update(self):
        self._unlink()
        self.blender_object = self._isosurface_object._create_mesh()
        self._link()

    def _unlink(self):
        bpy.data.collections["Collection"].objects.unlink(self.blender_object)
        bpy.data.objects.remove(self.blender_object, do_unlink=True)

    def _link(self):
        bpy.data.collections["Collection"].objects.link(self.blender_object)
        flip_normals(self.blender_object)


class VaspIsosurface:
    def __init__(self, filename, name, level=None, repetitions=(0, 0, 0)):
        self.name = name
        self.level = level
        self.repetitions = repetitions
        self.density = VaspChargeDensity(filename).chg[-1]
        self.unit_cell = VaspChargeDensity(filename).atoms[-1].cell
        self.blender_object = self._create_mesh()

    def _create_mesh(self):
        if self.repetitions != (0, 0, 0):
            repetitions = tuple([repetition + 1 for repetition in self.repetitions])
            self.unit_cell = diag(repetitions) @ self.unit_cell
            self.density = tile(self.density, repetitions)

        return marching_cubes_VASP(self.density, self.unit_cell, self.name, self.level)


class CubeIsosurface:
    def __init__(self, filename, name, level=None, repetitions=(0, 0, 0)):
        self.name = name
        self.level = level
        self.repetitions = repetitions
        self.density, self.origin, self.axes, *_ = read_cube(filename)
        self.blender_object = self._create_mesh()

    def _create_mesh(self):
        if self.repetitions != (0, 0, 0):
            repetitions = tuple([repetition + 1 for repetition in self.repetitions])
            self.density = tile(self.density, repetitions)

        return marching_cubes_gaussian(
            self.density, self.origin, self.axes, self.name, self.level
        )
