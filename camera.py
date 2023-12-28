import bpy  # type: ignore

from blentom.base import BlenderObject  # type: ignore


class Camera(BlenderObject):
    instance = None
    blender_object = None

    def __new__(cls, position=(0, 0, 20), rotation=(0, 0, 0)):
        if cls.instance is None:
            cls.instance = super(Camera, cls).__new__(cls)
            cls.blender_object = bpy.context.scene.camera
            cls.instance.position = position
            cls.instance.rotation = rotation
            cls.set_resolution((1080, 1080))
        return cls.instance

    @classmethod
    def set_resolution(cls, resolution):
        bpy.data.scenes["Scene"].render.resolution_x = resolution[0]
        bpy.data.scenes["Scene"].render.resolution_y = resolution[1]

    def render(self, filepath=None):
        if filepath is not None:
            bpy.context.scene.render.filepath = str(filepath)
            bpy.ops.render.render(write_still=True)
        else:
            bpy.ops.render.render()
