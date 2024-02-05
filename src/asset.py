from os.path import isabs
from pathlib import Path

import bpy

from .meshobject import MeshObject


class Asset(MeshObject):
    asset_directory = Path(__file__).parent / "resources" / "assets"

    def __init__(self, file):
        blender_object = Asset._load_asset(file)
        bpy.context.view_layer.objects.active = blender_object
        super().__init__()

    @classmethod
    def _load_asset(cls, file):
        if isabs(file):
            directory = Path(file) / "Object"
        else:
            directory = Asset.asset_directory / f"{file.lower()}.blend" / "Object"

        bpy.ops.wm.append(
            filepath="//Object/" + file,
            filename=file,
            directory=str(directory),
        )

        return bpy.data.objects.get(file)
