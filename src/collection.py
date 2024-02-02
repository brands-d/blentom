import bpy


class Collection:
    def __init__(self, name="New Collection"):
        if name in bpy.data.collections:
            self.collection = bpy.data.collections[name]
        else:
            self.collection = bpy.data.collections.new(name)
            bpy.context.scene.collection.children.link(self.collection)

    @property
    def name(self):
        return self.collection.name

    @name.setter
    def name(self, name):
        self.collection.name = name

    def __add__(self, objects):
        if not isinstance(objects, (list, tuple)):
            objects = (objects,)
        for object in objects:
            self.collection.objects.link(object.blender_object)
            self._unlink_from_scene_collections(object.blender_object)

        return self

    def link(self, collection):
        try:
            self.collection.children.link(collection.collection)
            bpy.context.scene.collection.children.unlink(collection.collection)
        except RuntimeError:
            pass

    def remove_object(self, objects):
        if not isinstance(objects, (list, tuple)):
            objects = (objects,)
        for object in objects:
            self.collection.objects.unlink(object.blender_object)

    def dissolve(self):
        for object in self.collection.objects:
            bpy.context.scene.collection.objects.link(object)
            self.collection.objects.unlink(object)

        bpy.data.collections.remove(self.collection)

    def _unlink_from_scene_collections(self, object):
        for collection in bpy.context.scene.collection.children:
            if collection.name != self.collection.name:
                if object.name in collection.objects:
                    collection.objects.unlink(object)

        if object.name in bpy.context.scene.collection.objects:
            bpy.context.scene.collection.objects.unlink(object)

    def delete(self):
        for object in self.collection.objects:
            object.delete()
        bpy.data.collections.remove(self.collection)
