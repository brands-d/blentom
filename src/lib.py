import bpy
from mathutils import Vector
from ase.io.cube import read_cube_data

from skimage.measure import marching_cubes as mc

BOHR = 0.529177
ANGSTROM = 1


def reset():
    bpy.ops.object.select_all(action="DESELECT")

    for object in bpy.context.scene.objects:
        if object.type == "MESH":
            bpy.data.objects.remove(object)

    for mesh in bpy.data.meshes:
        bpy.data.meshes.remove(mesh)

    for collection in bpy.data.collections:
        if collection.name != "Collection":
            bpy.data.collections.remove(collection)


def marching_cubes(density, unit_cell, name, level=None):
    vertices, faces, *_ = mc(density, level=level)
    vertices = [
        _vertex_transform(vertex, unit_cell, density.shape) for vertex in vertices
    ]
    edges = [[face[i], face[(i + 1) % 3]] for face in faces for i in range(3)]

    mesh = bpy.data.meshes.new(name=name)
    mesh.from_pydata(vertices, edges, faces)
    mesh.update()
    return bpy.data.objects.new(name, mesh)


def _vertex_transform(vertex, unit_cell, shape):
    new = (vertex[0] - 1) * unit_cell[0] / shape[0]
    new += (vertex[1] - 1) * unit_cell[1] / shape[1]
    new += (vertex[2] - 1) * unit_cell[2] / shape[2]
    return new


def flip_normals(object):
    bpy.context.view_layer.objects.active = object
    bpy.ops.object.mode_set(mode="OBJECT")
    object = bpy.context.active_object

    if object.type == "MESH":
        mesh = object.data
        for polygon in mesh.polygons:
            polygon.flip()

        mesh.update()

        bpy.ops.object.mode_set(mode="EDIT")
        bpy.ops.mesh.normals_make_consistent(inside=False)
        bpy.ops.object.mode_set(mode="OBJECT")


def read_cube(filename):
    with open(filename, "r") as file:
        lines = file.readlines()

    aux = [None, None, None, None]
    for i in range(0, 4):
        units, *axis = lines[i + 2].split()
        units = ANGSTROM if float(units) < 0 else BOHR
        aux[i] = Vector([float(i) * units for i in axis])

    origin, x, y, z = aux
    """
    units, *origin = lines[2].split()
    units = ANGSTROM if units < 0 else BOHR
    origin = Vector([float(i) * units for i in origin])
    _, *x_axis = lines[3].split()
    x_axis = Vector([float(x) * units for x in x_axis])
    _, *y_axis = lines[4].split()
    y_axis = Vector([float(y) * units for y in y_axis])
    _, *z_axis = lines[5].split()
    z_axis = Vector([float(z) * units for z in z_axis])
    """
    data, atoms = read_cube_data(filename)

    return data, origin, (x, y, z), atoms.cell
