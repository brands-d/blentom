import bpy
from sys import path, executable
from subprocess import check_call
from importlib.util import find_spec
from site import getusersitepackages

bl_info = {
    "name": "Blentom",
    "author": "Dominik Brandstetter",
    "email": "dominik.brandstetter@uni-graz.at",
    "license": "MIT",
    "version": (2, 0),
    "blender": (4, 0, 0),
    "description": "Import of common electronic structure files.",
    "doc_url": "https://github.com/brands-d/blentom/tree/main",
    "tracker_url": "https://github.com/brands-d/blentom/issues",
    "category": "Import-Export",
}

dependencies = (
    {"name": "ase", "import_name": "ase", "version": ""},
    {"name": "scikit-image", "import_name": "skimage", "version": ""},
)


def append_sitepackages_to_path():
    path.append(getusersitepackages())


def update_pip():
    check_call([executable, "-m", "pip", "install", "--user", "--upgrade", "pip"])


def install_dependency(dependency):
    check_call(
        [
            executable,
            "-m",
            "pip",
            "install",
            "--user",
            f"{dependency['name']}{dependency['version']}",
        ]
    )


def check_dependencies():
    first = True
    for dependency in dependencies:
        if not find_spec(dependency["import_name"]):
            if first:
                update_pip()
                first = False
            install_dependency(dependency)


append_sitepackages_to_path()
check_dependencies()

from .src import *


def register():
    bpy.utils.register_class(CubeImport)
    bpy.utils.register_class(XYZImport)
    bpy.utils.register_class(POSCARImport)
    bpy.utils.register_class(CHGCARImport)
    bpy.types.TOPBAR_MT_file_import.append(menu_func_import_cube)
    bpy.types.TOPBAR_MT_file_import.append(menu_func_import_xyz)
    bpy.types.TOPBAR_MT_file_import.append(menu_func_import_poscar)
    bpy.types.TOPBAR_MT_file_import.append(menu_func_import_chgcar)
    pass


def unregister():
    bpy.utils.unregister_class(CubeImport)
    bpy.utils.unregister_class(XYZImport)
    bpy.utils.unregister_class(POSCARImport)
    bpy.utils.unregister_class(CHGCARImport)
    bpy.types.TOPBAR_MT_file_import.remove(menu_func_import_cube)
    bpy.types.TOPBAR_MT_file_import.remove(menu_func_import_xyz)
    bpy.types.TOPBAR_MT_file_import.remove(menu_func_import_poscar)
    bpy.types.TOPBAR_MT_file_import.remove(menu_func_import_chgcar)
    pass
