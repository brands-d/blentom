from dependencies import install_dependencies

install_dependencies()

import bpy
from . import auto_load
from .src import *

bl_info = {
    "name": __name__,
    "author": __author__,
    "version": __version__,
    "blender": __blend_version__,
    "description": __description__,
    "doc_url": __url__,
    "tracker_url": __tracker__,
    "category": __category__,
}


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


if __name__ == "__main__":
    auto_load.init()
