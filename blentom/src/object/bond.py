import bpy  # type:ignore
from mathutils import Vector

from .meshobject import MeshObject

from ..utils.preset import Preset
from ..utils.lib import append_asset
from .. import __default_directory__, __user_directory__

# TODO: Go back to material indicies


class Bond(MeshObject):
    """
    Represents a bond between two atoms in a molecular structure.

    Attributes:
        atom_a (Atom): The first atom connected by the bond.
        atom_b (Atom): The second atom connected by the bond.
    """

    def __init__(self, atom_a, atom_b, double_bonds=False):
        """
        Initializes a Bond object between two atoms.

        Args:
            atom_a (Atom): The first atom connected by the bond.
            atom_b (Atom): The second atom connected by the bond.
            double_bonds (bool): Whether to display double and triple bonds.
        """
        self.atom_a = atom_a
        self.atom_b = atom_b
        self.atom_a.bonds.append(self)
        self.atom_b.bonds.append(self)

        vertices = Preset.get("bonds.sides")
        bpy.ops.mesh.primitive_cylinder_add(vertices=vertices)
        super().__init__()

        if Preset.get("bonds.smooth"):
            self.make_smooth()

        self._add_bond_logic(double_bonds)
        self._add_constraints()
        thickness = Preset.get("bonds.thickness")
        self.scale = (thickness, 1, thickness)

        # self.material = Preset.get("bonds.material")
        self.name = f"{atom_a.name}-{atom_b.name}"

    @property
    def thickness(self):
        """
        Get the thickness of the bond. Corresponds to the scaling.

        Returns:
            float: Thickness of the bond.
        """
        return self.blender_object.scale[0]

    @thickness.setter
    def thickness(self, thickness):
        """
        Set the thickness of the bond.

        Args:
            scale (float): Sets the thickness of the bond.
        """

        self.blender_object.scale = [thickness, thickness, self.scale[1]]

    @property
    def material(self):
        """
        Returns the material of the bond.

        Returns:
            Material: Material of the bond.
        """
        return self.material

    def _add_constraints(self):
        """
        Adds constraints to the bond setting its location onto one atom and makes it stretch to the other.
        """

        # Stretch modifier only works along the y-axis
        self.rotation = (90, 0, 0)
        self.apply_transformations("rotation")
        # Center of the bond that is fixed at atom A position needs to be the base of the cylinder
        self.location = (0, 1, 0)
        self.apply_transformations("location")

        bpy.ops.object.constraint_add(type="COPY_LOCATION")
        self.blender_object.constraints[
            "Copy Location"
        ].target = self.atom_a.blender_object

        bpy.ops.object.constraint_add(type="STRETCH_TO")
        self.blender_object.constraints[
            "Stretch To"
        ].target = self.atom_b.blender_object
        self.blender_object.constraints["Stretch To"].volume = "NO_VOLUME"
        self.blender_object.constraints["Stretch To"].keep_axis = "PLANE_X"
        # No idea but the bonds are too long otherwise
        self.blender_object.constraints["Stretch To"].rest_length = 2

    def _add_bond_logic(self, double_bonds):
        """
        Sets up complex geometry node logic for the bonds.
        """

        self._add_loop_cut()

        modifier_split = self.blender_object.modifiers.new(
            name="Bond Logic", type="NODES"
        )
        bpy.ops.node.new_geometry_node_group_assign()
        modifier_split.node_group.name = f"Bond - {self.name}"
        if "Bond" not in bpy.data.node_groups:
            append_asset(
                __default_directory__ / "assets.blend", "Bond", type_="NodeTree"
            )
        modifier_split.node_group = bpy.data.node_groups["Bond"]
        modifier_split["Socket_2"] = self.atom_a.blender_object
        modifier_split["Socket_3"] = self.atom_b.blender_object
        modifier_split["Socket_4"] = self.atom_a.material.material
        modifier_split["Socket_5"] = self.atom_b.material.material
        modifier_split["Socket_11"] = self.atom_a.covalent_radius
        modifier_split["Socket_12"] = self.atom_b.covalent_radius
        modifier_split["Socket_13"] = double_bonds
        modifier_split["Socket_14"] = double_bonds

    def _add_loop_cut(self):
        """
        Adds a loop cut around the long axis of a cylinder like object.
        """
        bpy.ops.object.mode_set(mode="EDIT")
        # From Blender info window, values are trial and error
        bpy.ops.mesh.loopcut_slide(
            MESH_OT_loopcut={
                "number_cuts": 1,
                "smoothness": 0,
                "falloff": "INVERSE_SQUARE",
                "object_index": 0,
                "edge_index": 3,
            }
        )
        bpy.ops.object.mode_set(mode="OBJECT")

    def make_smooth(self):
        """
        Use the smooth shader for this object.
        """
        self.blender_object.data.polygons.foreach_set(
            "use_smooth",
            [True] * len(self.blender_object.data.polygons),
        )

    @classmethod
    def _check_distance(cls, atom_a, atom_b, shift=(0, 0, 0)):
        """
        Check if the distance between two atoms is within the bonding threshold.

        Args:
            atom_a (Atom): The first atom.
            atom_b (Atom): The second atom.

        Returns:
            bool: True if the distance is within the bonding threshold, False otherwise.
        """
        factor = Preset.get("bonds.factor")
        position_a = Vector(atom_a.position)
        position_b = Vector(atom_b.position) + Vector(shift)
        radius_a = atom_a.covalent_radius
        radius_b = atom_b.covalent_radius

        return (position_a - position_b).length <= factor * (radius_a + radius_b)

    def delete(self):
        """
        Removes itself from bond lists of atoms participating in bond.
        """
        self.atom_a.bonds.remove(self)
        self.atom_b.bonds.remove(self)
