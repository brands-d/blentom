from subprocess import call
from sys import executable

import bpy

from . import auto_load
from .src import *

bl_info = {
    "name": "blentom",
    "author": "Dominik Brandstetter",
    "description": "",
    "blender": (4, 0, 0),
    "version": (0, 1, 0),
    "category": "Import-Export",
}


def menu_func_import_cube(self, context):
    self.layout.operator(CubeImport.bl_idname, text="Gaussian Cube (.cube)")


def menu_func_import_xyz(self, context):
    self.layout.operator(XYZImport.bl_idname, text="XYZ (.xyz)")


def menu_func_import_poscar(self, context):
    self.layout.operator(POSCARImport.bl_idname, text="POSCAR (POSCAR)")


def register():
    bpy.utils.register_class(CubeImport)
    bpy.utils.register_class(XYZImport)
    bpy.utils.register_class(POSCARImport)
    bpy.types.TOPBAR_MT_file_import.append(menu_func_import_cube)
    bpy.types.TOPBAR_MT_file_import.append(menu_func_import_xyz)
    bpy.types.TOPBAR_MT_file_import.append(menu_func_import_poscar)


def unregister():
    bpy.utils.unregister_class(CubeImport)
    bpy.utils.unregister_class(XYZImport)
    bpy.utils.unregister_class(POSCARImport)
    bpy.types.TOPBAR_MT_file_import.remove(menu_func_import_cube)
    bpy.types.TOPBAR_MT_file_import.remove(menu_func_import_xyz)
    bpy.types.TOPBAR_MT_file_import.remove(menu_func_import_poscar)


def install_dependencies():
    # On Windows Blender needs to run in Admin Mode
    py_exec = executable
    call([str(py_exec), "-m", "ensurepip", "--user"])
    call([str(py_exec), "-m", "pip", "install", "--upgrade", "pip"])
    call([str(py_exec), "-m", "pip", "install", "--user", "scikit-image"])
    call([str(py_exec), "-m", "pip", "install", "--user", "ase"])


if __name__ == "__main__":
    auto_load.init()
    install_dependencies()
