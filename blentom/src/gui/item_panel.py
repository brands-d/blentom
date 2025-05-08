from bpy.props import StringProperty, FloatProperty
from bpy.types import Operator, PropertyGroup, Panel

from ..object.isosurface import Isosurface


class IsosurfaceLevelItem(PropertyGroup):
    def get_level(self):
        for item in Isosurface.items:
            if item.blender_object is None:
                del item
                continue

            if item.name == self.name:
                return item.level / item.max

        return 0

    def set_level(self, value):
        for item in Isosurface.items:
            if item.name == self.name:
                item.level = value * item.max
                break

    name: StringProperty(name="Isosurface", default="Isosurface")
    level: FloatProperty(
        name="Level",
        default=0.10,
        min=0.01,
        max=0.99,
        step=0.01,
        precision=2,
        get=get_level,
        set=set_level,
    )


class SETTINGS_OT_add_isosurface_item(Operator):
    bl_idname = "blentom.add_isosurface_item"
    bl_label = "Add Isosurface Item"
    bl_options = {"REGISTER", "UNDO"}

    name: StringProperty(name="Name", default="Isosurface")
    level: FloatProperty(
        name="Level", default=0.10, min=0.0001, max=0.9999, step=0.001, precision=4
    )

    def execute(self, context):
        scene = context.scene
        isosurface = scene.item_panel_isosurfaces.add()
        isosurface.name = self.name
        isosurface.level = self.level

        return {"FINISHED"}


class ItemPanel(Panel):
    bl_idname = "OBJECT_PT_items"
    bl_label = "Items"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Blentom"

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        if len(scene.item_panel_isosurfaces) > 0:
            box = layout.box()

        for i, isosurface_item in enumerate(scene.item_panel_isosurfaces):
            row = box.row(align=True)
            row.prop(isosurface_item, "level", text=f"{isosurface_item.name} Level")
