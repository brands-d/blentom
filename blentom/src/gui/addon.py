import bpy
from bpy.types import Operator, AddonPreferences

from subprocess import Popen

from ..utils.preset import Preset
from ..utils.material import Material
from ..utils.periodic_table import Element
from ..utils.lib import open_in_text_editor
from .. import __default_directory__, __user_directory__


class ADDONPREFS_OT_open_default_directory(Operator):
    """Open the default directory"""

    bl_idname = "object.blentom_open_default_directory"
    bl_label = "Open Default Directory"
    bl_description = str(__default_directory__)
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        Popen(f'explorer "{__default_directory__}"')
        return {"FINISHED"}


class ADDONPREFS_OT_open_user_directory(Operator):
    """Opens the user directory"""

    bl_idname = "object.blentom_open_user_directory"
    bl_label = "Open User Directory"
    bl_description = str(__user_directory__)
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        Popen(f'explorer "{__user_directory__}"')
        return {"FINISHED"}


class ADDONPREFS_OT_open_elements(Operator):
    """Open the elements user file"""

    bl_idname = "object.blentom_open_elements"
    bl_label = "Open Elements User File"
    bl_description = str(Element.elements_user_file)
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        Element.ensure_user_file()
        open_in_text_editor(Element.elements_user_file, context)

        return {"FINISHED"}


class ADDONPREFS_OT_open_presets(Operator):
    """Open the presets user file"""

    bl_idname = "object.blentom_open_presets"
    bl_label = "Open Presets User File"
    bl_description = str(Preset.presets_user_file)
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        Preset.ensure_user_file()
        open_in_text_editor(Preset.presets_user_file, context)

        return {"FINISHED"}


class ADDONPREFS_OT_open_materials(Operator):
    """Open the materials user file"""

    bl_idname = "object.blentom_open_materials"
    bl_label = "Open Materials User File"
    bl_description = str(Material.materials_user_file)
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        Material.ensure_user_file()
        if bpy.data.is_dirty:
            self.report(
                {"WARNING"}, "Unsaved changes in the current file. Save before opening."
            )
        else:
            bpy.ops.wm.open_mainfile(
                filepath=str(Material.materials_user_file), check_existing=True
            )

        return {"FINISHED"}


class BlentomInformation(AddonPreferences):
    bl_idname = __package__.rsplit(".", 2)[0]

    def draw(self, context):
        layout = self.layout

        layout.label(text="Directories:")
        row = layout.row()
        split = row.split(factor=0.5)
        split.column().operator(ADDONPREFS_OT_open_default_directory.bl_idname)
        split.column().operator(ADDONPREFS_OT_open_user_directory.bl_idname)

        layout.label(text="Files:")
        row = layout.row()
        split = row.split(factor=1 / 3)
        split.column().operator(ADDONPREFS_OT_open_materials.bl_idname)
        split.column().operator(ADDONPREFS_OT_open_presets.bl_idname)
        split.column().operator(ADDONPREFS_OT_open_elements.bl_idname)


class OBJECT_OT_blentom_preferences(Operator):
    """Display example preferences"""

    bl_idname = "object.blentom_preferences"
    bl_label = "Blentom Preferences"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        return {"FINISHED"}
