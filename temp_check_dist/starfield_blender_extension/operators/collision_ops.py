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

import math
import typing

from .. import utils
from ..utils import bs_plugin_data


class BGS_STARFIELD_OT_create_rigidbody(bpy.types.Operator):
    bl_label = "Create Rigidbody"
    bl_idname = bs_plugin_data.bl_id_with_project_suffix(
        "bgs_starfield.create_rigidbody")
    bl_description = "Creates a rigidbody on the selected object. A rigidbody can have many colliders."
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bs_plugin_data.object_get_bgs_rigidbody(
            context.active_object).is_rigidbody = True
        if bs_plugin_data.object_get_bgs_collider(context.active_object).is_collider == True:
            context.active_object.display.show_shadows = True
            context.active_object.hide_render = False
            context.active_object.display_type = "TEXTURED"
        return {'FINISHED'}


class BGS_STARFIELD_OT_remove_rigidbody(bpy.types.Operator):
    bl_label = "Remove Rigidbody"
    bl_idname = bs_plugin_data.bl_id_with_project_suffix(
        "bgs_starfield.remove_rigidbody")
    bl_description = "Removes the rigidbody from the selected object."
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bs_plugin_data.object_get_bgs_rigidbody(
            context.active_object).is_rigidbody = False
        return {'FINISHED'}


class BGS_STARFIELD_OT_create_collider(bpy.types.Operator):
    bl_label = "Create Collider"
    bl_idname = bs_plugin_data.bl_id_with_project_suffix(
        "bgs_starfield.create_collider")
    bl_description = "Creates a collider geometry from the selected mesh. A rigidbody can have many colliders."
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        col_obj = context.active_object
        bs_plugin_data.object_get_bgs_collider(col_obj).is_collider = True
        if bs_plugin_data.object_get_bgs_rigidbody(col_obj).is_rigidbody == False:
            col_obj.display.show_shadows = False
            col_obj.hide_render = True
            col_obj.display_type = "WIRE"
            col_obj.color = (.8, 0.1, 0, 1)
        return {'FINISHED'}


class BGS_STARFIELD_OT_remove_collider(bpy.types.Operator):
    bl_label = "Remove Collider"
    bl_idname = bs_plugin_data.bl_id_with_project_suffix(
        "bgs_starfield.remove_collider")
    bl_description = "Removes the collider geometry from the selected object."
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        col_obj = context.active_object
        bs_plugin_data.object_get_bgs_collider(col_obj).is_collider = False
        col_obj.display.show_shadows = True
        col_obj.hide_render = False
        col_obj.display_type = "TEXTURED"
        return {'FINISHED'}


class BGS_STARFIELD_OT_add_constraint_to_rigidbody(bpy.types.Operator):
    bl_idname = bs_plugin_data.bl_id_with_project_suffix(
        "bgs_starfield.add_constraint_to_rigidbody")
    bl_label = "Add Constraint to Rigidbody"
    bl_description = "Add Constraint to rigidbody"

    def invoke(self, context, event):
        bs_plugin_data.object_get_bgs_rigidbody(context.obj).constraints.add()
        return {'FINISHED'}


class BGS_STARFIELD_OT_remove_constraint_from_rigidbody(bpy.types.Operator):
    bl_idname = bs_plugin_data.bl_id_with_project_suffix(
        "bgs_starfield.remove_constraint_from_rigidbody")
    bl_label = "Remove Constraint Sequence"
    bl_description = "Remove this animation sequence from scene"

    index: bpy.props.IntProperty()  # type: ignore

    def invoke(self, context, event):
        bs_plugin_data.object_get_bgs_rigidbody(
            context.obj).constraints.remove(self.index)
        return {'FINISHED'}


class BGS_STARFIELD_OT_copy_transform_to_constraint(bpy.types.Operator):
    bl_idname = bs_plugin_data.bl_id_with_project_suffix(
        "bgs_starfield.copy_transform_to_constraint"
    )
    bl_label = "Copy Transform to Constraint"
    bl_description = "Copy Transform to Constraint"

    index: bpy.props.IntProperty()  # type: ignore

    def invoke(self, context, event):
        obj = context.active_object
        constraint = bs_plugin_data.object_get_bgs_rigidbody(
            obj).constraints[self.index]
        constraint.child_space_translation = obj.location
        constraint.child_space_rotation_e = obj.rotation_euler
        if constraint.connected_node is not None:
            constraint.parent_space_translation = constraint.connected_node.location
            constraint.parent_space_rotation_e = constraint.connected_node.rotation_euler
        return {'FINISHED'}


def register():
    bpy.utils.register_class(BGS_STARFIELD_OT_create_rigidbody)
    bpy.utils.register_class(BGS_STARFIELD_OT_remove_rigidbody)
    bpy.utils.register_class(BGS_STARFIELD_OT_create_collider)
    bpy.utils.register_class(BGS_STARFIELD_OT_remove_collider)
    bpy.utils.register_class(BGS_STARFIELD_OT_add_constraint_to_rigidbody)
    bpy.utils.register_class(BGS_STARFIELD_OT_remove_constraint_from_rigidbody)
    bpy.utils.register_class(BGS_STARFIELD_OT_copy_transform_to_constraint)

def unregister():
    bpy.utils.unregister_class(BGS_STARFIELD_OT_create_rigidbody)
    bpy.utils.unregister_class(BGS_STARFIELD_OT_remove_rigidbody)
    bpy.utils.unregister_class(BGS_STARFIELD_OT_create_collider)
    bpy.utils.unregister_class(BGS_STARFIELD_OT_remove_collider)
    bpy.utils.unregister_class(BGS_STARFIELD_OT_add_constraint_to_rigidbody)
    bpy.utils.unregister_class(BGS_STARFIELD_OT_remove_constraint_from_rigidbody)
    bpy.utils.unregister_class(BGS_STARFIELD_OT_copy_transform_to_constraint)
