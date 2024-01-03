bl_info = {
    "name": "Gaussian Cube Import",
    "blender": (3, 0, 0),
    "category": "Import-Export",
}

import bpy
import numpy as np
from skimage.measure import marching_cubes

bond_threshold = 1.2

# Materials
H_material = bpy.data.materials.new(name="H")
C_material = bpy.data.materials.new(name="C")
N_material = bpy.data.materials.new(name="N")
O_material = bpy.data.materials.new(name="O")
positive_material = bpy.data.materials.new(name="Positive")
negative_material = bpy.data.materials.new(name="Negative")

materials = [
    H_material,
    C_material,
    N_material,
    O_material,
    positive_material,
    negative_material,
]

for material in materials:
    material.use_nodes = True
    material.node_tree.nodes["Principled BSDF"].inputs[2].default_value[0] = 1.5
    material.node_tree.nodes["Principled BSDF"].inputs[2].default_value[1] = 1.5
    material.node_tree.nodes["Principled BSDF"].inputs[2].default_value[2] = 1.5

H_material.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (1, 1, 1, 1)
H_material.node_tree.nodes["Principled BSDF"].inputs[6].default_value = 0
H_material.node_tree.nodes["Principled BSDF"].inputs[9].default_value = 0
H_material.node_tree.nodes["Principled BSDF"].inputs[10].default_value = 0.1
H_material.node_tree.nodes["Principled BSDF"].inputs[19].default_value = (1, 1, 1, 1)
H_material.node_tree.nodes["Principled BSDF"].inputs[20].default_value = 0

C_material.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (0, 0, 0, 1)
C_material.node_tree.nodes["Principled BSDF"].inputs[6].default_value = 0.5
C_material.node_tree.nodes["Principled BSDF"].inputs[7].default_value = 0.2
C_material.node_tree.nodes["Principled BSDF"].inputs[9].default_value = 0.3
C_material.node_tree.nodes["Principled BSDF"].inputs[10].default_value = 0.1
C_material.node_tree.nodes["Principled BSDF"].inputs[14].default_value = 0.25
C_material.node_tree.nodes["Principled BSDF"].inputs[15].default_value = 0
C_material.node_tree.nodes["Principled BSDF"].inputs[19].default_value = (
    0.00495756,
    0.00495756,
    0.00495756,
    1,
)
C_material.node_tree.nodes["Principled BSDF"].inputs[20].default_value = 0

O_material.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (1, 0, 0, 1)
O_material.node_tree.nodes["Principled BSDF"].inputs[6].default_value = 0.5
O_material.node_tree.nodes["Principled BSDF"].inputs[7].default_value = 0.2
O_material.node_tree.nodes["Principled BSDF"].inputs[9].default_value = 0.5
O_material.node_tree.nodes["Principled BSDF"].inputs[10].default_value = 0.1
O_material.node_tree.nodes["Principled BSDF"].inputs[14].default_value = 0
O_material.node_tree.nodes["Principled BSDF"].inputs[15].default_value = 0
O_material.node_tree.nodes["Principled BSDF"].inputs[19].default_value = (1, 0, 0, 1)
O_material.node_tree.nodes["Principled BSDF"].inputs[20].default_value = 0

positive_material.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (
    1,
    0,
    0,
    1,
)
positive_material.node_tree.nodes["Principled BSDF"].inputs[1].default_value = 0.5
positive_material.node_tree.nodes["Principled BSDF"].inputs[2].default_value = [1, 1, 1]
positive_material.node_tree.nodes["Principled BSDF"].inputs[3].default_value = (
    1,
    0.1,
    0.1,
    1,
)
positive_material.node_tree.nodes["Principled BSDF"].inputs[6].default_value = 0
positive_material.node_tree.nodes["Principled BSDF"].inputs[7].default_value = 0.5
positive_material.node_tree.nodes["Principled BSDF"].inputs[9].default_value = 1
positive_material.node_tree.nodes["Principled BSDF"].inputs[10].default_value = 0
positive_material.node_tree.nodes["Principled BSDF"].inputs[14].default_value = 0
positive_material.node_tree.nodes["Principled BSDF"].inputs[15].default_value = 1
positive_material.node_tree.nodes["Principled BSDF"].inputs[19].default_value = (
    1,
    0,
    0,
    1,
)
positive_material.node_tree.nodes["Principled BSDF"].inputs[20].default_value = 0.2
positive_material.node_tree.nodes["Principled BSDF"].inputs[20].default_value = 0.7

negative_material.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (
    0,
    0,
    1,
    1,
)
negative_material.node_tree.nodes["Principled BSDF"].inputs[1].default_value = 0.5
negative_material.node_tree.nodes["Principled BSDF"].inputs[2].default_value = [1, 1, 1]
negative_material.node_tree.nodes["Principled BSDF"].inputs[3].default_value = (
    0.1,
    0.1,
    1,
    1,
)
negative_material.node_tree.nodes["Principled BSDF"].inputs[6].default_value = 0
negative_material.node_tree.nodes["Principled BSDF"].inputs[7].default_value = 0.5
negative_material.node_tree.nodes["Principled BSDF"].inputs[9].default_value = 1
negative_material.node_tree.nodes["Principled BSDF"].inputs[10].default_value = 0
negative_material.node_tree.nodes["Principled BSDF"].inputs[14].default_value = 0
negative_material.node_tree.nodes["Principled BSDF"].inputs[15].default_value = 1
negative_material.node_tree.nodes["Principled BSDF"].inputs[19].default_value = (
    0,
    0,
    1,
    1,
)
negative_material.node_tree.nodes["Principled BSDF"].inputs[20].default_value = 0.2
negative_material.node_tree.nodes["Principled BSDF"].inputs[20].default_value = 0.7

# Information about different elements
# Atomic number: (symbol, color, radius [bohr], covalent radius [bohr])
atom_sorts = {
    "H": (1, H_material, 0.42, 0.64),
    "C": (6, C_material, 1, 1.54),
    "O": (8, O_material, 0.95, 1.46),
}


def load_cube_file(context, filepath, use_cube_setting):
    origin, axes, atoms, wavefunction, bonds = read_cube_data(filepath)

    objects = {"wavefunctions": [], "atoms": {}}
    sorts = add_atoms(atoms, objects)
    add_wavefunction(wavefunction, axes, origin, objects)
    add_bonds(bonds, atoms)

    return {"FINISHED"}


def add_bonds(bonds, atoms):
    bond_collection = bpy.data.collections.new("Bonds")
    bpy.context.scene.collection.children.link(bond_collection)
    for bond in bonds:
        atom_i, atom_j = atoms[bond[0]][2], atoms[bond[1]][2]
        distance = atom_j - atom_i
        location = atom_i + distance / 2
        bpy.ops.mesh.primitive_cylinder_add(radius=0.30, vertices=25, location=location)
        bond_object = bpy.context.object
        bond_object.name = f"Bond {bond[0]:d}-{bond[1]:d}"
        bpy.context.scene.collection.objects.unlink(bond_object)
        bond_collection.objects.link(bond_object)
        bond_object.rotation_euler[1] = np.arccos(
            distance[2] / np.linalg.norm(distance)
        )
        bond_object.rotation_euler[2] = np.arctan2(distance[1], distance[0])
        bond_object.data.polygons.foreach_set(
            "use_smooth", [True] * len(bond_object.data.polygons)
        )


def add_wavefunction(wavefunction, axes, origin, objects, levels=(0.02, -0.02)):
    wf_collection = bpy.data.collections.new("Wavefunctions")
    bpy.context.scene.collection.children.link(wf_collection)
    for level in levels:
        wf_object = add_partial_wavefunction(
            wavefunction, axes, level, origin, wf_collection
        )
        wf_collection.objects.link(wf_object)
        objects["wavefunctions"].append(wf_object)


def add_atoms(atoms, objects):
    sorts = set([atom[0] for atom in atoms])
    for sort in sorts:
        objects["atoms"].update({sort: []})

    atom_collection = bpy.data.collections.new("Atoms")
    bpy.context.scene.collection.children.link(atom_collection)
    for atom in atoms:
        atom_object = add_atom(atom, atom_collection)
        bpy.context.scene.collection.objects.unlink(atom_object)
        atom_collection.objects.link(atom_object)
        objects["atoms"][atom[0]].append(atom_object)

    for sort in sorts:
        for atom in objects["atoms"][sort]:
            atom.select_set(True)

        bpy.context.view_layer.objects.active = objects["atoms"][sort][0]
        bpy.context.view_layer.objects.active.data.materials.append(atom_sorts[sort][1])
        bpy.ops.object.make_links_data(type="OBDATA")

        for atom in objects["atoms"][sort]:
            atom.select_set(False)

    return sorts


def density_to_isosurface(density, axes, level, origin=(0, 0, 0)):
    vertices, faces, normals, values = marching_cubes(volume=density, level=level)
    vertices = [
        [np.dot(axes[i], vertex) + origin[i] for i in (0, 1, 2)] for vertex in vertices
    ]
    edges = []
    for face in faces:
        edges.append([face[0], face[1]])
        edges.append([face[1], face[2]])
        edges.append([face[2], face[0]])

    return (vertices, edges, faces)


def add_atom(atom, col):
    sort, _, location = atom
    radius = atom_sorts[sort][2]
    bpy.ops.mesh.primitive_uv_sphere_add(
        segments=16, ring_count=16, radius=radius, location=location
    )
    atom_object = bpy.context.object
    atom_object.name = sort
    atom_object.data.polygons.foreach_set(
        "use_smooth", [True] * len(atom_object.data.polygons)
    )

    return atom_object


def add_partial_wavefunction(wavefunction, axes, level, origin, col):
    name = "Positive" if level > 0 else "Negative"
    isosurface = density_to_isosurface(wavefunction, axes, level, origin)
    mesh = bpy.data.meshes.new(name=name)
    mesh.from_pydata(*isosurface)
    mesh.update()

    wf_object = bpy.data.objects.new(name, mesh)
    if level > 0:
        wf_object.data.materials.append(positive_material)
    else:
        wf_object.data.materials.append(negative_material)

    wf_object.modifiers.new(name="Remesh", type="REMESH")
    wf_object.modifiers["Remesh"].mode = "VOXEL"
    wf_object.modifiers["Remesh"].voxel_size = 0.2
    wf_object.modifiers["Remesh"].use_smooth_shade = True

    return wf_object


def read_cube_data(filepath):
    with open(filepath, "r") as file:
        lines = file.readlines()

    atom_num, origin_x, origin_y, origin_z = lines[2].split()
    atom_num, origin = int(atom_num), (
        float(origin_x),
        float(origin_y),
        float(origin_z),
    )

    atoms = []
    for i in range(atom_num):
        sort, charge, atom_x, atom_y, atom_z = lines[i + 6].split()

        found = False
        for key, value in atom_sorts.items():
            sort = int(sort)
            if value[0] == sort:
                found = True
                atoms.append(
                    [
                        key,
                        charge,
                        np.array([float(atom_x), float(atom_y), float(atom_z)]),
                    ]
                )
                break

        if not found:
            raise TypeError(f"Atom sort {sort:.0f} not available")

    eof = False
    wavefunction = []
    x_num, xx, xy, xz = lines[3].split()
    x_num, x_axis = int(x_num), (float(xx), float(xy), float(xz))
    y_num, yx, yy, yz = lines[4].split()
    y_num, y_axis = int(y_num), (float(yx), float(yy), float(yz))
    z_num, zx, zy, zz = lines[5].split()
    z_num, z_axis = int(z_num), (float(zx), float(zy), float(zz))

    for line in lines[atom_num + 6 :]:
        wavefunction += [float(x) for x in line.split()]

    wavefunction = np.array(wavefunction).reshape((x_num, y_num, z_num))

    bonds = []
    for i, atom_i in enumerate(atoms):
        for j, atom_j in enumerate(atoms):
            if i == j:
                continue

            distance = np.linalg.norm(atom_i[2] - atom_j[2])
            radius_i = atom_sorts[atom_i[0]][3]
            radius_j = atom_sorts[atom_j[0]][3]
            if distance <= bond_threshold * (radius_i + radius_j):
                bonds.append((i, j))

    return origin, (x_axis, y_axis, z_axis), atoms, wavefunction, bonds


# ImportHelper is a helper class, defines filename and
# invoke() function which calls the file selector.
from bpy_extras.io_utils import ImportHelper
from bpy.props import StringProperty, BoolProperty, EnumProperty
from bpy.types import Operator


class GaussianCubeImportAddon(Operator, ImportHelper):
    bl_idname = "import_test.cube"
    bl_label = "Import Cube File"

    filename_ext = ".cube"

    filter_glob: StringProperty(
        default="*.cube",
        options={"HIDDEN"},
        maxlen=255,
    )

    # List of operator properties, the attributes will be assigned
    # to the class instance from the operator settings before calling.
    use_setting: BoolProperty(
        name="Example Boolean",
        description="Example Tooltip",
        default=True,
    )

    type: EnumProperty(
        name="Example Enum",
        description="Choose between two items",
        items=(
            ("OPT_A", "First Option", "Description one"),
            ("OPT_B", "Second Option", "Description two"),
        ),
        default="OPT_A",
    )

    def execute(self, context):
        return load_cube_file(context, self.filepath, self.use_setting)


def menu_func_import(self, context):
    self.layout.operator(GaussianCubeImportAddon.bl_idname, text="Cube File (.cube)")


def register():
    bpy.utils.register_class(GaussianCubeImportAddon)
    bpy.types.TOPBAR_MT_file_import.append(menu_func_import)


def unregister():
    bpy.utils.unregister_class(GaussianCubeImportAddon)
    bpy.types.TOPBAR_MT_file_import.remove(menu_func_import)


if __name__ == "__main__":
    register()

    bpy.ops.import_test.cube("INVOKE_DEFAULT")
