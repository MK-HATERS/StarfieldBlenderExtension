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


class BGS_STARFIELD_OT_toggle_armature_bone_sgo_keep(bpy.types.Operator):
    bl_label = "Toggle \"SGO Keep\" on bone"
    bl_idname = bs_plugin_data.bl_id_with_project_suffix(
        "bgs_starfield.toggle_armature_bone_sgo_keep")
    bl_description = "Toggle \"SGO Keep\" on bone"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        arm = context.arm
        bone = context.bone

        armature_props = bs_plugin_data.armature_get_bgs_props(arm)
        armature_bone_property = None
        if armature_props:
            for itr_armature_bone_property in armature_props.armature_bone_properties:
                if itr_armature_bone_property.name == bone.name:
                    armature_bone_property = itr_armature_bone_property
                    break

        if armature_bone_property == None:
            armature_bone_property = armature_props.armature_bone_properties.add()
            armature_bone_property.name = bone.name
            armature_bone_property.sgo_keep = False

        armature_bone_property.sgo_keep = not armature_bone_property.sgo_keep

        return {'FINISHED'}


def register():
    bpy.utils.register_class(BGS_STARFIELD_OT_toggle_armature_bone_sgo_keep)

def unregister():
    bpy.utils.unregister_class(BGS_STARFIELD_OT_toggle_armature_bone_sgo_keep)
