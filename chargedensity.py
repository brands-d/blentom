from numpy import array
import bpy  # type: ignore
from ase.io.cube import read_cube_data
from blentom.material import Material  # type: ignore
from mathutils import Vector  # type: ignore
from ase.calculators.vasp import VaspChargeDensity
from skimage.measure import marching_cubes

from blentom.base import BlenderObject  # type: ignore


class ChargeDensity(BlenderObject):
    def __init__(
        self, density, axes, origin, level=0.5, cell=((1, 0, 0), (0, 1, 0), (0, 0, 1))
    ):
        self.level = level
        self.cell = cell
        name = "Charge Density"
        vertices, faces, *_ = marching_cubes(density, level=level)
        vertices = [
            [Vector(vertex).dot(Vector(axes[i])) + origin[i] for i in range(3)]
            for vertex in vertices
        ]
        edges = [[face[i], face[(i + 1) % 3]] for face in faces for i in range(3)]

        mesh = bpy.data.meshes.new(name=name)
        mesh.from_pydata(vertices, edges, faces)
        mesh.update()
        self.blender_object = bpy.data.objects.new(name, mesh)
        self.blender_object.modifiers.new(name="Remesh", type="REMESH")
        self.blender_object.modifiers["Remesh"].mode = "VOXEL"
        self.blender_object.modifiers["Remesh"].voxel_size = 0.2
        self.blender_object.modifiers["Remesh"].use_smooth_shade = True
        bpy.data.collections["Collection"].objects.link(self.blender_object)

        self.material = Material.pre_defined(f"Charge Density")

    @classmethod
    def read(cls, filename, level=0.5):
        density = VaspChargeDensity(filename).chg[-1]
        cell = VaspChargeDensity(filename).atoms[-1].cell
        coordinates = coordinate(cell, density.shape)
        axes = array([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
        origin = (0, 0, 0)
        return ChargeDensity(density, axes, origin, level=level, cell=cell)


def transform(coordinate, cell, shape):
    new = (coordinate[0] - 1) * cell[0] / shape[0]
    new += (coordinate[1] - 1) * cell[1] / shape[1]
    new += (coordinate[2] - 1) * cell[2] / shape[2]
    return new


def make_mesh(vertices, edges, faces):
    mesh = bpy.data.meshes.new(name="Density")
    mesh.from_pydata(vertices, edges, faces)
    mesh.update()
    object = bpy.data.objects.new("Density", mesh)
    object.modifiers.new(name="Remesh", type="REMESH")
    object.modifiers["Remesh"].mode = "VOXEL"
    object.modifiers["Remesh"].voxel_size = 0.2
    object.modifiers["Remesh"].use_smooth_shade = True
    bpy.data.collections["Collection"].objects.link(object)
