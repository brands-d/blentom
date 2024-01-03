import bpy  # type: ignore
from mathutils import Vector  # type: ignore

from ase.io.cube import read_cube_data
from skimage.measure import marching_cubes

from .material import Material
from .base import BlenderObject


class WavefunctionPart(BlenderObject):
    def __init__(
        self,
        data,
        origin,
        axes,
        level=0.02,
        cell=((1, 0, 0), (0, 1, 0), (0, 0, 1)),
        **kwargs,
    ):
        self.level = level
        self.cell = cell
        name = "Positive" if level > 0 else "Negative"
        vertices, faces, *_ = marching_cubes(data, level=level)
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

        self.material = Material.pre_defined(f"{name} Wavefunction")
        super().__init__(**kwargs)


class Wavefunction:
    def __init__(
        self, data, origin, axes, level=0.02, cell=((1, 0, 0), (0, 1, 0), (0, 0, 1))
    ):
        self.wavefunction_parts = []
        self.cell = cell
        for sign in (-1, 1):
            self.wavefunction_parts.append(
                WavefunctionPart(data, origin, axes, sign * level, cell)
            )

    @classmethod
    def read(cls, filename, level=0.05):
        data, origin, axes, cell = Wavefunction._parse_cube(filename)
        wavefunction = Wavefunction(data, origin, axes, level=level, cell=cell)
        return wavefunction

    @property
    def positive(self):
        return self.wavefunction_parts[1]

    @property
    def negative(self):
        return self.wavefunction_parts[0]

    def periodic(self, periodicity=False):
        for wavefunction_part in self.wavefunction_parts:
            wavefunction_part.periodic(periodicity, self.cell)

    @classmethod
    def _parse_cube(cls, filename):
        with open(filename, "r") as file:
            lines = file.readlines()

        _, *origin = lines[2].split()
        origin = Vector([float(i) for i in origin])
        _, *x_axis = lines[3].split()
        x_axis = Vector([float(x) for x in x_axis])
        _, *y_axis = lines[4].split()
        y_axis = Vector([float(y) for y in y_axis])
        _, *z_axis = lines[5].split()
        z_axis = Vector([float(z) for z in z_axis])

        data, atoms = read_cube_data(filename)

        return data, origin, (x_axis, y_axis, z_axis), atoms.cell
