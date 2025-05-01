from shutil import copy
from os.path import exists

import bpy

from ..utils import append_asset
from .periodic_table import PeriodicTable
from .. import __default_directory__, __user_directory__


class Material:
    """A class representing a material in Blender.

    Attributes:
        materials_directory (Path): The directory where the material files are located.
        materials_default_file (Path): The file with the default materials.
        materials_user_file (Path): The file containing the user materials.
    """

    materials_default_file = __default_directory__ / "assets.blend"
    materials_user_file = __user_directory__ / "assets_user.blend"

    def __init__(self, name):
        """
        Get an existing Blender material object. If the material does not exist, tries to load it from a materials file. User file is preferred. If the material is not found in any file, creates a new material.

        Args:
            name (str): The name of the material.
        """

        # Less than 3 characters is probably an element symbol
        if len(name) <= 2:
            try:
                name = PeriodicTable.get(name).name
            except KeyError:
                pass

        material = bpy.data.materials.get(name)
        if material is None:
            try:
                Material.load(name)
            except (ValueError, RuntimeError):
                Material._create(name)

        self.blender_material = bpy.data.materials.get(name)

    @property
    def name(self):
        """
        Get the name of the material.

        Returns:
            str: The name of the material.
        """
        return self.blender_material.name

    @name.setter
    def name(self, name):
        """
        Set the name of the material.

        Args:
            name (str): The name of the material.
        """
        self.blender_material.name = name

    @property
    def material(self):
        """
        Get the material object.

        Returns:
            bpy.types.Material: The material object.
        """
        return self.blender_material

    @material.setter
    def material(self, material):
        """
        Set the material object.

        Args:
            material (bpy.types.Material): The material object.
        """
        self.blender_material = material

    @property
    def color(self):
        """
        Base color of the material.

        Returns:
            tuple[float]: RGBA values between 0 and 1.
        """
        try:
            return self.properties["Base Color"]
        except KeyError:
            try:
                return self.properties["Color"]
            except KeyError:
                return (1, 1, 1, 1)

    @color.setter
    def color(self, color):
        """
        Sets the base color of the material.

        Args:
            color (tuple[float]): RGBA values between 0 and 1.
        """
        self.properties = {"Base Color": color}

    @classmethod
    def _create(cls, name):
        material = bpy.data.materials.new(name=name)
        material.use_nodes = True
        material.use_backface_culling = True
        material.blend_method = "BLEND"
        material.node_tree.nodes["Principled BSDF"]

    @property
    def properties(self):
        """
        Get the properties of the material.

        Note:
            Only possible if material has a Principled BSDF node.

        Returns:
            dict: The properties of the material.

        Raises:
            RuntimeError: Principled BSDF node is not found.
        """
        properties = {}
        try:
            shader = self.blender_material.node_tree.nodes["Principled BSDF"]
        except KeyError:
            shader = None
            for node in self.blender_material.node_tree.nodes:
                if node.type == "BSDF_PRINCIPLED":
                    shader = node
                    break
                elif node.type == "BSDF_GLOSSY":
                    shader = node
                    break
            if shader is None:
                raise RuntimeError("Principled BSDF node not found")

        for input in shader.inputs:
            properties[input.name] = input.default_value

        return properties

    @properties.setter
    def properties(self, properties):
        """
        Set the properties of the material.

        Note:
            Only possible to Principled BSDF node properties.

        Args:
            properties (dict): The properties to set.

        Raises:
            RuntimeError: Principled BSDF node is not found.
        """
        try:
            shader = self.blender_material.node_tree.nodes["Principled BSDF"]
        except KeyError:
            for node in self.blender_material.node_tree.nodes:
                if node.type == "BSDF_PRINCIPLED":
                    shader = node
                    break
            if shader is None:
                raise RuntimeError("Principled BSDF node not found")

        for property, value in properties.items():
            try:
                shader.inputs[property].default_value = value
            except KeyError:
                raise KeyError(f"Property {property} not found")

    @property
    def shader(self):
        """
        Get the shader node of the material.

        Returns:
            bpy.types.Node: The shader node.
        """
        try:
            return self.blender_material.node_tree.nodes["Principled BSDF"]
        except KeyError:
            for node in self.blender_material.node_tree.nodes:
                if node.type == "BSDF_PRINCIPLED":
                    return node
                elif node.type == "BSDF_GLOSSY":
                    return node
            return None

    def edit(self, property, value):
        """
        Edit a property of the material.

        Args:
            property (str): The property to edit.
            value (any): The new value for the property.
        """
        try:
            shader = self.blender_material.node_tree.nodes["Principled BSDF"]
        except KeyError:
            for node in self.blender_material.node_tree.nodes:
                if node.type == "BSDF_PRINCIPLED":
                    shader = node
                    break
            if shader is None:
                raise KeyError("Principled BSDF node not found.")

        try:
            shader.inputs[property].default_value = value
        except KeyError:
            raise KeyError(f"Property {property} not found.")

    @classmethod
    def material_exists(cls, material):
        """
        Checks whether material exists.

        Args:
            material (str): Name of the material.

        Returns:
            bool: True if material exists.
        """
        return bpy.data.materials.get(material) is not None

    @classmethod
    def load(cls, name):
        """
        Load a material from material files. User file is preferred.

        Args:
            name (str): The name of the material to load.

        Raises:
            RuntimeError: If the material file is not found.
            ValueError: If the specified material is not found in the file.
        """
        cls.ensure_user_file()
        append_asset(cls.materials_user_file, name, type_="Material")
        if not cls.material_exists(name):
            append_asset(cls.materials_default_file, name, type_="Material")

    @classmethod
    def _check_user_file_exists(cls):
        """
        Check if the user material file exists.

        Returns:
            bool: True if the user material file exists, False otherwise.
        """
        return exists(cls.materials_user_file)

    @classmethod
    def ensure_user_file(cls):
        """
        Ensures that the user-specific materials file exists. If the file does not exist,
        it copies the default materials file to the user-specific location.
        """
        if not cls._check_user_file_exists():
            copy(cls.materials_default_file, cls.materials_user_file)
