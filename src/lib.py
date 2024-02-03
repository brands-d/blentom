import bpy

from skimage.measure import marching_cubes as mc


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
