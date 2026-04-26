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
import typing
import math
from .. import utils
from ..utils import bs_plugin_data


class BGS_STARFIELD_OT_add_vertex_group_partition(bpy.types.Operator):
    bl_label = "Add BGS Partition to Vertex Group"
    bl_idname = bs_plugin_data.bl_id_with_project_suffix(
        "bgs_starfield.add_vertex_group_partition")
    bl_description = "Add BGS Partition to Vertex Group"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        obj = context.obj
        vertex_group = context.vertex_group

        for i in range(
                0, len(bs_plugin_data.object_get_bgs_vertex_group_partitions(obj).partitions)):
            itr_vertex_group_partition = bs_plugin_data.object_get_bgs_vertex_group_partitions(
                obj).partitions[i]
            if itr_vertex_group_partition.vertex_group_index == vertex_group.index:
                return {'FINISHED'}

        vertex_group_partition = bs_plugin_data.object_get_bgs_vertex_group_partitions(
            obj).partitions.add()
        vertex_group_partition.vertex_group_index = vertex_group.index
        return {'FINISHED'}


class BGS_STARFIELD_OT_remove_vertex_group_partition(bpy.types.Operator):
    bl_label = "Remove BGS Partition from Vertex Group"
    bl_idname = bs_plugin_data.bl_id_with_project_suffix(
        "bgs_starfield.remove_vertex_group_partition")
    bl_description = "Remove BGS Partition from Vertex Group"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        obj = context.obj
        vertex_group = context.vertex_group

        for i in range(
                0, len(bs_plugin_data.object_get_bgs_vertex_group_partitions(obj).partitions)):
            itr_vertex_group_partition = bs_plugin_data.object_get_bgs_vertex_group_partitions(
                obj).partitions[i]
            if itr_vertex_group_partition.vertex_group_index == vertex_group.index:
                bs_plugin_data.object_get_bgs_vertex_group_partitions(
                    obj).partitions.remove(i)
                return {'FINISHED'}

        return {'FINISHED'}


def register():
    bpy.utils.register_class(BGS_STARFIELD_OT_add_vertex_group_partition)
    bpy.utils.register_class(BGS_STARFIELD_OT_remove_vertex_group_partition)

def unregister():
    bpy.utils.unregister_class(BGS_STARFIELD_OT_add_vertex_group_partition)
    bpy.utils.unregister_class(BGS_STARFIELD_OT_remove_vertex_group_partition)
