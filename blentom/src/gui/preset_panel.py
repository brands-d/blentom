import bpy
from bpy.types import Operator
# from bpy.props import EnumProperty

# from ..utils.preset import Preset

my_custom_items = [
    ("ITEM_A", "First Option", "This is the first custom choice", "CUBE", 0),
    ("ITEM_B", "Second Option", "This is the second custom choice", "SPHERE", 1),
    ("ITEM_C", "Third Option", "This is the third custom choice", "MONKEY", 2),
    # Add more items here as needed
]


# Function called when dropdown changes (optional)
def update_custom_selection(self, context):
    print(f"Custom selection changed to: {self.my_custom_enum_prop}")
    # Add any logic needed when the selection changes


# Define the custom property on the Scene
bpy.types.Scene.my_custom_enum_prop = bpy.props.EnumProperty(
    items=my_custom_items,
    name="Custom Item",  # This label is mostly internal now
    description="Select a custom item",
    default="ITEM_A",
    update=update_custom_selection,
)


class OBJECT_OT_duplicate_preset(Operator):
    """Duplicate the current preset"""

    bl_idname = "object.blentom_duplicate_preset"
    bl_label = "Duplicate"
    bl_description = "Create a copy of the current preset"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        # Only enable if an item is selected (or based on your logic)
        return context.scene.my_custom_enum_prop is not None

    def execute(self, context):
        selected_id = context.scene.my_custom_enum_prop
        self.report({"INFO"}, f"Duplicate requested for: {selected_id}")

        global my_custom_items
        my_custom_items += [
            ("ITEM_D", "Fourth Option", "This is the fourth custom choice", "CUBE", 3)
        ]
        return {"FINISHED"}


class PresetPanel(bpy.types.Panel):
    bl_idname = "OBJECT_PT_preset"
    bl_label = "Presets"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Blentom"

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        row = layout.row()
        split = row.split(factor=0.85)
        split.column().prop(scene, "my_custom_enum_prop", text="")
        split.column().operator(
            OBJECT_OT_duplicate_preset.bl_idname, text="", icon="DUPLICATE"
        )


class CurrentPresetPanel(bpy.types.Panel):
    bl_idname = "OBJECT_PT_current_preset"
    bl_label = "Preset Settings"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Blentom"
    bl_parent_id = "OBJECT_PT_preset"

    def draw(self, context):
        layout = self.layout

        row = layout.row()
        row.operator("object.select_all").action = "INVERT"
        row.operator("object.select_all").action = "INVERT"

        box = layout.box()
        box.label(text="Current Preset")
        box.operator("object.select_all").action = "TOGGLE"
        row = box.row()
        row.operator("object.select_all").action = "INVERT"
        row.operator("object.select_random")
