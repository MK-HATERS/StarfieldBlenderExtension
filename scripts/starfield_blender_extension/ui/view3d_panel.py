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

from .object_panel import VIEW3D_PT_bgs_starfield_object
from .collision_panel import VIEW3D_PT_bgs_starfield_collision
from .animation_panel import VIEW3D_PT_bgs_starfield_animation
from .general_panel import VIEW3D_PT_bgs_starfield_general
from ..operators.export_ops import BGS_STARFIELD_OT_set_recommended_unit_scale
from ..utils import bs_plugin_data

# FUNCTIONS


def draw_option(layout, opt, obj=None, enabled=True):
    row = layout.row(align=True)
    if obj is None:
        obj = bpy.context.scene
    row.prop(obj, opt)
    row.enabled = enabled

# PANELS


class VIEW3D_PT_bgs_starfield_export(bpy.types.Panel):
    bl_idname = bs_plugin_data.bl_id_with_project_suffix(
        "VIEW3D_PT_bgs_starfield_export")
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_label = " "

    @classmethod
    def poll(cls, context):
        return context.mode == 'OBJECT'

    def draw(self, context):
        layout = self.layout
        layout.separator()

        layout.use_property_split = False
        layout.use_property_decorate = False

        box = layout.box()
        box.scale_x = .75

        # box.operator("bgs_starfield.do_bsfbx_export", text="Export as BGS FBX", icon='NODETREE')
        box.operator(bs_plugin_data.bl_id_with_project_suffix(
            "bgs_starfield.verify_scene_data_and_do_export"), text="Export as BSFBX", icon='NODETREE')
        box.prop(context.scene,
                 bs_plugin_data.scene_export_config_prop_name(), text="Config")
        box.prop(bs_plugin_data.scene_get_bs_fbx_export_settings(
            context.scene), "selected_only")
        box.prop(bs_plugin_data.scene_get_bs_fbx_export_settings(
            context.scene), "export_centered_at_origin")

        box.prop(bs_plugin_data.scene_get_bs_fbx_export_settings(
            context.scene), "show_additional_settings")
        if bs_plugin_data.scene_get_bs_fbx_export_settings(context.scene).show_additional_settings:
            box.prop(bs_plugin_data.scene_get_bs_fbx_export_settings(
                context.scene), "starfield_export_scale")


class VIEW3D_PT_bgs_starfield(bpy.types.Panel):
    bl_idname = bs_plugin_data.bl_id_with_project_suffix(
        "VIEW3D_PT_bgs_starfield")
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'BGS Starfield'
    bl_label = "BGS Starfield"
    bl_options = {'HIDE_HEADER'}

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = False
        layout.use_property_decorate = False

        layout.label(text="BGS Blender Tools (Starfield)")

        row = layout.row(align=True)
        row.prop(
            context.scene, bs_plugin_data.scene_bgs_starfield_panel_tab_prop_name(), expand=True)

        if bs_plugin_data.scene_get_bgs_starfield_panel_tab(context.scene) == 'OBJECT':
            VIEW3D_PT_bgs_starfield_general.draw(self, context)
        elif bs_plugin_data.scene_get_bgs_starfield_panel_tab(context.scene) == 'COLLISION':
            VIEW3D_PT_bgs_starfield_collision.draw(self, context)
        elif bs_plugin_data.scene_get_bgs_starfield_panel_tab(context.scene) == 'ANIMATION':
            VIEW3D_PT_bgs_starfield_animation.draw(self, context)
        elif bs_plugin_data.scene_get_bgs_starfield_panel_tab(context.scene) == 'EXPORT':
            if context.mode != 'OBJECT':
                layout.label(text="Exit Edit Mode to change settings")
                return
            VIEW3D_PT_bgs_starfield_export.draw(self, context)


def register():
    bpy.utils.register_class(VIEW3D_PT_bgs_starfield)

def unregister():
    bpy.utils.unregister_class(VIEW3D_PT_bgs_starfield)
