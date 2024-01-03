from pathlib import Path
from src.atom import Atoms
from src.light import Light
from src.camera import Camera
from src.wavefunction import Wavefunction
from src.plane import Plane
from src.base import reset
from src.material import Material
from src.chargedensity import ChargeDensity
from skimage.measure import marching_cubes
import bpy
from ase.calculators.vasp import VaspChargeDensity
from mathutils import Matrix, Vector

reset()

dir_ = Path("/Users/dominik/Desktop/blentom/demo")

#atom = Atoms.read("demo/CHGCAR")

file = VaspChargeDensity("demo/CHGCAR")
density = file.chg[-1]
cell = file.atoms[-1].cell
vertices, faces, *_ = marching_cubes(density,level=0.55) #0.55
cell_scaled = cell/density.shape
vertices = [Matrix(cell_scaled).transposed() @ Vector(vertex) for vertex in vertices]
edges = [[face[i], face[(i + 1) % 3]] for face in faces for i in range(3)]



mesh = bpy.data.meshes.new(name="Density")
mesh.from_pydata(vertices, edges, faces)
mesh.update()
object = bpy.data.objects.new("Density", mesh)
object.modifiers.new(name="Remesh", type="REMESH")
object.modifiers["Remesh"].mode = "VOXEL"
object.modifiers["Remesh"].voxel_size = 0.2
object.modifiers["Remesh"].use_smooth_shade = True
bpy.data.collections["Collection"].objects.link(object)