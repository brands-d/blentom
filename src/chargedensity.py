import bpy  # type: ignore

from numpy import array
from ase.calculators.vasp import VaspChargeDensity
from skimage.measure import marching_cubes

from .material import Material
from .base import BlenderObject


class ChargeDensity(BlenderObject):
    def __init__(self, density, cell, level=0.5):
        self.level = level
        self.cell = cell
        name = "Charge Density"
        vertices, faces, *_ = marching_cubes(density, level=level)
        vertices = [transform(vertex, cell, density.shape) for vertex in vertices]
        edges = [[face[i], face[(i + 1) % 3]] for face in faces for i in range(3)]

        mesh = bpy.data.meshes.new(name=name)
        mesh.from_pydata(vertices, edges, faces)
        mesh.update()
        self.blender_object = bpy.data.objects.new(name, mesh)
        bpy.data.collections["Collection"].objects.link(self.blender_object)

        self.material = Material.pre_defined(f"Charge Density")

    @classmethod
    def read(cls, filename, level=0.5):
        density = VaspChargeDensity(filename).chg[-1]
        cell = VaspChargeDensity(filename).atoms[-1].cell
        return ChargeDensity(density, cell, level=level)


def transform(vertex, cell, shape):
    new = (vertex[0] - 1) * cell[0] / shape[0]
    new += (vertex[1] - 1) * cell[1] / shape[1]
    new += (vertex[2] - 1) * cell[2] / shape[2]
    return new
