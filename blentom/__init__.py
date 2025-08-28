from bpy.props import CollectionProperty
from bpy.types import TOPBAR_MT_file_import, Scene
from bpy.utils import register_class, unregister_class


from .src import *  # noqa: F403
from .src.io import *  # noqa: F403
from .src.gui import *  # noqa: F403

importhelper = [
    CubeImport,
    XYZImport,
    POSCARImport,
    CHGCARImport,
    DatabaseImport,
]

operators = [
    SETTINGS_OT_add_isosurface_item,
    OBJECT_OT_blentom_preferences,
    # OBJECT_OT_duplicate_preset,
    ADDONPREFS_OT_open_materials,
    ADDONPREFS_OT_open_default_directory,
    ADDONPREFS_OT_open_user_directory,
    ADDONPREFS_OT_open_elements,
    ADDONPREFS_OT_open_presets,
]

panels = [
    # ItemPanel,
    # PresetPanel,
    # CurrentPresetPanel,
]

other = [BlentomInformation, IsosurfaceLevelItem]

menu_items = [
    menu_func_import_cube,
    menu_func_import_xyz,
    menu_func_import_poscar,
    menu_func_import_chgcar,
    menu_func_import_database,
]


def register():
    for cls in importhelper:
        register_class(cls)
    for cls in operators:
        register_class(cls)
    # for cls in panels:
    #    register_class(cls)
    for cls in other:
        register_class(cls)
    for cls in menu_items:
        TOPBAR_MT_file_import.append(cls)  # noqa: F405

    Scene.item_panel_isosurfaces = CollectionProperty(type=IsosurfaceLevelItem)


def unregister():
    for cls in importhelper:
        unregister_class(cls)
    for cls in operators:
        unregister_class(cls)
    for cls in panels:
        unregister_class(cls)
    for cls in other:
        unregister_class(cls)
    for cls in menu_items:
        TOPBAR_MT_file_import.remove(cls)  # noqa: F405
