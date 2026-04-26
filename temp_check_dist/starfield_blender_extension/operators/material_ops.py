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
import os
from ..utils import bs_plugin_data

from .. import utils


class BGS_STARFIELD_OT_load_path_material(bpy.types.Operator):
    bl_label = "Load textures to blender material"
    bl_idname = bs_plugin_data.bl_id_with_project_suffix(
        "bgs_starfield.load_path_material")
    bl_description = "Load loose textures from Starfield Data folder (defined in Addon preferences) to Blender Material."
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        target_mat = context.active_object.active_material
        if target_mat is None:
            return {'CANCELLED'}
        if not target_mat.use_nodes:
            utils.show_message_box("(Failed) material does not use nodes")
            return {'CANCELLED'}

        starfield_data_path = utils.get_starfield_data_path_with_trailing_slash()

        if not os.path.isdir(starfield_data_path):
            utils.show_message_box(
                "Addon preferences-defined starfield data directory does not exist(%s)" %
                (starfield_data_path))
            return {'CANCELLED'}

        diffuse_path = starfield_data_path + \
            bs_plugin_data.material_get_bgs_props(target_mat).texture_diffuse
        normal_path = starfield_data_path + \
            bs_plugin_data.material_get_bgs_props(target_mat).texture_normal

        if not os.path.isfile(diffuse_path):
            utils.show_message_box(
                "Diffuse texture not found (%s)" % (diffuse_path))
            return {'CANCELLED'}

        if not os.path.isfile(normal_path):
            utils.show_message_box(
                "Diffuse texture not found (%s)" % (normal_path))
            return {'CANCELLED'}

        target_mat.node_tree.links.clear()
        target_mat.node_tree.nodes.clear()

        tex_diffuse = target_mat.node_tree.nodes.new(type='ShaderNodeTexImage')
        tex_normal = target_mat.node_tree.nodes.new(type='ShaderNodeTexImage')
        node_shader = target_mat.node_tree.nodes.new(
            type='ShaderNodeBsdfPrincipled')
        output = target_mat.node_tree.nodes.new(
            type='ShaderNodeOutputMaterial')

        tex_diffuse.image = bpy.data.images.load(diffuse_path)
        tex_normal.image = bpy.data.images.load(normal_path)

        target_mat.node_tree.links.new(tex_diffuse.outputs.get(
            "Color"), node_shader.inputs.get("Base Color"))
        target_mat.node_tree.links.new(tex_normal.outputs.get(
            "Color"), node_shader.inputs.get("Normal"))
        target_mat.node_tree.links.new(node_shader.outputs.get(
            "BSDF"), output.inputs.get("Surface"))

        return {'FINISHED'}


def register():
    bpy.utils.register_class(BGS_STARFIELD_OT_load_path_material)

def unregister():
    bpy.utils.unregister_class(BGS_STARFIELD_OT_load_path_material)
