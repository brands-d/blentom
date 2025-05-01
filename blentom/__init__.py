from bpy.utils import register_class, unregister_class
from bpy.types import TOPBAR_MT_file_import

from .src import *  # noqa: F403
from .src.gui import *  # noqa: F403
from .src.io import *  # noqa: F403


def register():
    register_class(CubeImport)  # noqa: F405
    register_class(XYZImport)  # noqa: F405
    register_class(POSCARImport)  # noqa: F405
    register_class(CHGCARImport)  # noqa: F405
    register_class(DatabaseImport)  # noqa: F405
    register_class(BlentomInformation)  # noqa: F405
    register_class(OBJECT_OT_blentom_preferences)  # noqa: F405
    register_class(ADDONPREFS_OT_open_materials)  # noqa: F405
    register_class(ADDONPREFS_OT_open_default_directory)  # noqa: F405
    register_class(ADDONPREFS_OT_open_user_directory)  # noqa: F405
    register_class(ADDONPREFS_OT_open_elements)  # noqa: F405
    register_class(ADDONPREFS_OT_open_presets)  # noqa: F405

    # File Import Menu Items
    TOPBAR_MT_file_import.append(menu_func_import_cube)  # noqa: F405
    TOPBAR_MT_file_import.append(menu_func_import_xyz)  # noqa: F405
    TOPBAR_MT_file_import.append(menu_func_import_poscar)  # noqa: F405
    TOPBAR_MT_file_import.append(menu_func_import_chgcar)  # noqa: F405
    TOPBAR_MT_file_import.append(menu_func_import_database)  # noqa: F405


def unregister():
    unregister_class(CubeImport)  # noqa: F405
    unregister_class(XYZImport)  # noqa: F405
    unregister_class(POSCARImport)  # noqa: F405
    unregister_class(CHGCARImport)  # noqa: F405
    unregister_class(DatabaseImport)  # noqa: F405
    unregister_class(BlentomInformation)  # noqa: F405
    unregister_class(OBJECT_OT_blentom_preferences)  # noqa: F405
    unregister_class(ADDONPREFS_OT_open_materials)  # noqa: F405
    unregister_class(ADDONPREFS_OT_open_default_directory)  # noqa: F405
    unregister_class(ADDONPREFS_OT_open_user_directory)  # noqa: F405
    unregister_class(ADDONPREFS_OT_open_elements)  # noqa: F405
    unregister_class(ADDONPREFS_OT_open_presets)  # noqa: F405

    # File Import Menu Items
    TOPBAR_MT_file_import.remove(menu_func_import_cube)  # noqa: F405
    TOPBAR_MT_file_import.remove(menu_func_import_xyz)  # noqa: F405
    TOPBAR_MT_file_import.remove(menu_func_import_poscar)  # noqa: F405
    TOPBAR_MT_file_import.remove(menu_func_import_chgcar)  # noqa: F405
    TOPBAR_MT_file_import.remove(menu_func_import_database)  # noqa: F405
