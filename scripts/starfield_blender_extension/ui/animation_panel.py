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

from .. import utils
from ..utils import bs_plugin_data


class BGS_STARFIELD_OT_set_add_animation_sequence(bpy.types.Operator):
    bl_idname = bs_plugin_data.bl_id_with_project_suffix(
        "bgs_starfield.add_animation_sequence")
    bl_label = "Add Animation Sequence"
    bl_description = "Add animation sequence to scene"

    def invoke(self, context, event):
        bs_plugin_data.scene_get_animation_sequences(context.scene).add()
        return {'FINISHED'}


class BGS_STARFIELD_OT_set_remove_animation_sequence(bpy.types.Operator):
    bl_idname = bs_plugin_data.bl_id_with_project_suffix(
        "bgs_starfield.remove_animation_sequence")
    bl_label = "Remove Animation Sequence"
    bl_description = "Remove this animation sequence from scene"

    index: bpy.props.IntProperty()  # type: ignore

    def invoke(self, context, event):
        bs_plugin_data.scene_get_animation_sequences(
            context.scene).remove(self.index)
        return {'FINISHED'}


class VIEW3D_PT_bgs_starfield_animation(bpy.types.Panel):
    bl_idname = bs_plugin_data.bl_id_with_project_suffix(
        "VIEW3D_PT_bgs_starfield_animation")
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_label = " "

    def draw(self, context):
        layout = self.layout
        layout.separator()
        box = layout.box()
        box.operator(bs_plugin_data.bl_id_with_project_suffix(
            "bgs_starfield.add_animation_sequence"), icon="PLUS", text="Add Sequence")

        for i in range(0, len(bs_plugin_data.scene_get_animation_sequences(context.scene))):
            seq = bs_plugin_data.scene_get_animation_sequences(context.scene)[
                i]
            row = box.row()
            row.prop(seq, "name", text="Name")
            row.prop(seq, "start_frame", text="Start")
            row.prop(seq, "end_frame", text="End")
            row.prop(seq, "loop", text="Loop")
            row.operator(bs_plugin_data.bl_id_with_project_suffix(
                "bgs_starfield.remove_animation_sequence"), icon="X", text="").index = i


def register():
    bpy.utils.register_class(BGS_STARFIELD_OT_set_add_animation_sequence)
    bpy.utils.register_class(BGS_STARFIELD_OT_set_remove_animation_sequence)

def unregister():
    bpy.utils.unregister_class(BGS_STARFIELD_OT_set_remove_animation_sequence)
    bpy.utils.unregister_class(BGS_STARFIELD_OT_set_add_animation_sequence)
