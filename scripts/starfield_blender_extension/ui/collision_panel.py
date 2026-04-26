# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

# Script copyright (C) 2024, Zenimax Media

import bpy

from ..utils import collision
from ..utils import bgs
from ..utils import bs_plugin_data


class VIEW3D_PT_bgs_starfield_collision(bpy.types.Panel):
    bl_idname = bs_plugin_data.bl_id_with_project_suffix(
        "VIEW3D_PT_bgs_starfield_collision")
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_label = " "

    def draw(self, context):
        layout = self.layout
        layout.separator()
        obj = context.active_object

        if obj == None:
            return

        if bs_plugin_data.object_get_bgs_collider(obj).is_collider:
            box = layout.box()
            box.context_pointer_set("obj", obj)

            box.label(text="Collider Geometry")
            box.operator(bs_plugin_data.bl_id_with_project_suffix(
                "bgs_starfield.remove_collider"), icon='TRASH')
            box.separator()
            box.prop(bs_plugin_data.object_get_bgs_collider(obj), "type")
            box.prop(bs_plugin_data.object_get_bgs_collider(obj), "layer")
            box.prop(bs_plugin_data.object_get_bgs_collider(obj), "material")
            if int(bs_plugin_data.object_get_bgs_collider(obj).material) == bgs.custom_enum_value():
                box.prop(bs_plugin_data.object_get_bgs_collider(
                    obj), "custom_material")
            box.prop(bs_plugin_data.object_get_bgs_collider(obj), "part")
        else:
            layout.operator(bs_plugin_data.bl_id_with_project_suffix(
                "bgs_starfield.create_collider"), icon='RESTRICT_SELECT_OFF')

        if bs_plugin_data.object_get_bgs_rigidbody(obj).is_rigidbody:
            box = layout.box()
            box.context_pointer_set("obj", obj)

            box.label(text="Rigidbody")
            box.operator(bs_plugin_data.bl_id_with_project_suffix(
                "bgs_starfield.remove_rigidbody"), icon='TRASH')
            box.separator()

            box.label(text="Child Colliders: %d" %
                      (len(collision.get_collider_children(obj))))
            box.prop(bs_plugin_data.object_get_bgs_rigidbody(obj), "mass",
                     icon='PHYSICS')
            box.prop(bs_plugin_data.object_get_bgs_rigidbody(obj), "friction",
                     icon='PHYSICS')
            box.prop(bs_plugin_data.object_get_bgs_rigidbody(obj), "restitution",
                     icon='PHYSICS')
            box.prop(bs_plugin_data.object_get_bgs_rigidbody(obj),
                     "unyielding", text="Unyielding (Keyframed)")

            box.prop(bs_plugin_data.object_get_bgs_rigidbody(
                obj), "has_bone_proxy", text="Bone Proxy",
                icon='BONE')
            if bs_plugin_data.object_get_bgs_rigidbody(obj).has_bone_proxy:
                bone_proxy_box = box.box()
                bone_proxy_box.prop(bs_plugin_data.object_get_bgs_rigidbody(
                    obj), "bone_proxy_armature", text="Armature")
                bone_proxy_box.prop(bs_plugin_data.object_get_bgs_rigidbody(
                    obj), "bone_proxy_name", text="Bone Name")

            box.label(text="Constraints: %d" % (
                len(bs_plugin_data.object_get_bgs_rigidbody(obj).constraints)))
            box.operator(bs_plugin_data.bl_id_with_project_suffix(
                "bgs_starfield.add_constraint_to_rigidbody"),
                text="Add Constraint", icon='CONSTRAINT')

            for i in range(0, len(bs_plugin_data.object_get_bgs_rigidbody(obj).constraints)):
                itr_constraint = bs_plugin_data.object_get_bgs_rigidbody(
                    obj).constraints[i]
                box_parent = box
                box = box.box()
                box.prop(itr_constraint, "type", text="Type")
                box.prop(itr_constraint, "connected_node",
                         text="Connected Node")
                box.operator(bs_plugin_data.bl_id_with_project_suffix(
                    "bgs_starfield.copy_transform_to_constraint"),
                    text="Copy Transform to Constraint", icon='COPYDOWN').index = i

                box.prop(itr_constraint, "child_space_translation",
                         text="Translation (Child)")
                box.prop(itr_constraint, "child_space_rotation_e",
                         text="Rotation (Child)")

                box.prop(itr_constraint, "parent_space_translation",
                         text="Translation (Parent)")
                box.prop(itr_constraint, "parent_space_rotation_e",
                         text="Rotation (Parent)")

                if itr_constraint.type == "RAGDOLL":
                    box.prop(itr_constraint, "ragdoll_cone_min_angle",
                             text="Cone Min Angle")
                    box.prop(itr_constraint, "ragdoll_max_friction_torque",
                             text="Max Friction Torque")
                    box.prop(itr_constraint, "ragdoll_plane_max_angle",
                             text="Plane Max Angle")
                    box.prop(itr_constraint, "ragdoll_plane_min_angle",
                             text="Plane Min Angle")
                    box.prop(itr_constraint, "ragdoll_twist_max_angle",
                             text="Twist Max Angle")
                    box.prop(itr_constraint, "ragdoll_twist_min_angle",
                             text="Twist Min Angle")
                elif itr_constraint.type == "HINGE":
                    box.prop(itr_constraint, "hinge_limited", text="Limited")
                    box.prop(itr_constraint, "hinge_min_angle",
                             text="Min Angle")
                    box.prop(itr_constraint, "hinge_max_angle",
                             text="Max Angle")
                    box.prop(itr_constraint, "hinge_max_friction_torque",
                             text="Max Friction Torque")
                elif itr_constraint.type == "PRISMATIC":
                    box.prop(itr_constraint, "prismatic_is_limited_min",
                             text="Limited Min")
                    box.prop(itr_constraint, "prismatic_is_limited_max",
                             text="Limited Max")
                    box.prop(itr_constraint, "prismatic_min_linear_limit",
                             text="Min Linear Limit")
                    box.prop(itr_constraint, "prismatic_max_linear_limit",
                             text="Max Linear Limit")
                    box.prop(itr_constraint, "prismatic_max_friction_force",
                             text="Max Friction Force")

                box.operator(bs_plugin_data.bl_id_with_project_suffix(
                    "bgs_starfield.remove_constraint_from_rigidbody"),
                    text="Remove Constraint", icon='TRASH').index = i
                box = box_parent
        else:
            layout.operator(bs_plugin_data.bl_id_with_project_suffix(
                "bgs_starfield.create_rigidbody"), icon='PARTICLES')


