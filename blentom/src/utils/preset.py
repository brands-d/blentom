from shutil import copy
from os.path import exists
from json import dump as jdump
from json import load as jload

from .. import __default_directory__, __user_directory__
from .utils import deep_dict_update


class Preset:
    """
    A class representing a preset configuration for Blender. This includes but
    is not limited to size of atoms objects, renderer settings and lighting.

    Attributes:
        preset (str): The currently selected preset.
        presets (dict): A dictionary containing loaded presets.
        presets_default_file (Path): The file with the default presets.
        presets_user_file (Path): The file containing the user presets.
    """

    preset = None
    presets = {}
    presets_default_file = __default_directory__ / "presets.json"
    presets_user_file = __user_directory__ / "presets_user.json"

    @classmethod
    def reload(cls):
        """
        Reloads the presets files.
        """

        cls.presets = Preset._read(user=False)
        cls.presets = deep_dict_update(cls.presets, Preset._read(user=True))

    @classmethod
    def _read(cls, user=True):
        """
        Reads and loads preset data from a JSON file.
        Args:
            user (bool, optional): Determines which file to read from.
                If True, reads from the user-specific presets file.
                If False, reads from the default presets file. Defaults to True.
        Returns:
            dict: The loaded preset data from the specified JSON file.
        """

        if user:
            cls.ensure_user_file()
            path = Preset.presets_user_file
        else:
            path = Preset.presets_default_file

        return jload(open(path))

    @classmethod
    def get(cls, setting, preset=None):
        """
        Retrieves the value of a specific setting from a preset.

        Args:
            setting (str): The setting to retrieve, in the format "group.[subgroup.[subsubgroup.]]property".
            preset (str | None): The preset from which the property should be returned. Default: Currently loaded preset.

        Returns:
            The value of the specified property.

        Examples:
            >>> # Returns the preset material (name) for Carbon atoms
            >>> Preset.get("atoms.carbon.material")
            >>> # Returns the preset size of all bonds
            >>> Preset.get("bonds.size")
            >>> # Returns the resolution of the "default" preset
            >>> Preset.get("camera.resolution", preset="default")
        """
        preset = Preset.preset if preset is None else preset
        # Preset._reload_presets()

        # Use default as backup if a property is not defined
        aux = Preset.presets["default"]
        aux = deep_dict_update(aux, Preset.presets[preset])

        setting = setting.split(".")
        if len(setting) == 2:
            # No subgroup
            group, property = setting
            return aux[group][property]
        elif len(setting) == 3:
            # Subgroup
            group, subgroup, property = setting
            return aux[group][subgroup][property]
        elif len(setting) == 4:
            # Subsubgroup
            group, subgroup, subsubgroup, property = setting
            return aux[group][subgroup][subsubgroup][property]
        else:
            raise ValueError(
                "Wrong setting format. Use: group.[subgroup.[subsubgroup.]]property"
            )

    @classmethod
    def set(cls, setting, value, preset=None):
        """
        Sets the value of a specific property in a preset. Edits the user preset file!

        Args:
            setting (str): The property to set, in the format "group.[subgroup.[subsubgroup.]]property".
            value (any): The value to set for the specified property.
            preset (str | None): The preset for which the property should be set. Default: Currently loaded preset.

        Examples:
            >>> # Sets the scale for carbon atoms in the "default" preset
            >>> Preset.set("atoms.carbon.scale", 1.2, preset="default")
        """
        preset = Preset.preset if preset is None else preset
        user_preset = Preset._read(user=True)

        setting = setting.split(".")
        if len(setting) == 2:
            # No subgroup
            group, property = setting
            user_preset = deep_dict_update(
                user_preset, {preset: {group: {property: value}}}
            )
        elif len(setting) == 3:
            # Subgroup
            group, subgroup, property = setting
            user_preset = deep_dict_update(
                user_preset, {preset: {group: {subgroup: {property: value}}}}
            )
        elif len(setting) == 4:
            # Subsubgroup
            group, subgroup, subsubgroup, property = setting
            user_preset = deep_dict_update(
                user_preset,
                {preset: {group: {subgroup: {subsubgroup: {property: value}}}}},
            )
        else:
            raise ValueError(
                "Wrong setting format. Use: group.[subgroup.[subsubgroup.]]property"
            )

        jdump(user_preset, open(Preset.presets_user_file, "w"))

    @classmethod
    def _check_user_file_exists(cls):
        """
        Checks if the user presets file exists.

        Returns:
            bool: True if the user presets file exists, False otherwise.
        """

        return exists(cls.presets_user_file)

    @classmethod
    def ensure_user_file(cls):
        """
        Ensures the existence of the user presets file.
        This method checks if the user presets file exists. If it does not exist,
        it copies the default presets file to create the user presets file.
        """

        if not cls._check_user_file_exists():
            copy(cls.presets_default_file, cls.presets_user_file)


Preset.reload()
Preset.preset = "default"
