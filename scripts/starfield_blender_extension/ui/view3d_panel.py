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

        # Export Options Section
        options_box = layout.box()
        options_box.label(text="Export Options", icon='EXPORT')

        # Export Type Selection
        row = options_box.row()
        row.label(text="Export Type:")
        row.prop(context.scene, bs_plugin_data.scene_export_config_prop_name(), text="")

        # Export Directory
        options_box.prop(bs_plugin_data.scene_get_bs_fbx_export_settings(
            context.scene), "export_directory", text="Export Directory")

        # Export Settings Section
        settings_box = layout.box()
        settings_box.label(text="Export Settings", icon='SETTINGS')

        col = settings_box.column(align=True)
        col.prop(bs_plugin_data.scene_get_bs_fbx_export_settings(
            context.scene), "starfield_export_scale", text="Scale")
        col.prop(bs_plugin_data.scene_get_bs_fbx_export_settings(
            context.scene), "compression_border", text="Compression Border")
        col.prop(bs_plugin_data.scene_get_bs_fbx_export_settings(
            context.scene), "selected_only", text="Selected Objects Only")
        col.prop(bs_plugin_data.scene_get_bs_fbx_export_settings(
            context.scene), "export_centered_at_origin", text="Centered at Origin")

        # Export Datatypes Section
        datatypes_box = layout.box()
        datatypes_box.label(text="Export Datatypes", icon='MESH_DATA')

        col = datatypes_box.column(align=True)

        # Get current export config to determine which settings to show
        config = getattr(context.scene, bs_plugin_data.scene_export_config_prop_name())

        # Geometry export controls
        if config in ["Static", "Furniture", "Container", "Weapon"]:
            col.prop(bs_plugin_data.scene_get_bs_fbx_export_settings(
                context.scene), "external_geometry", text="Geometry: External")

            # External Geometry sub-settings
            if bs_plugin_data.scene_get_bs_fbx_export_settings(context.scene).external_geometry:
                sub_col = col.column(align=True)
                sub_col.prop(bs_plugin_data.scene_get_bs_fbx_export_settings(
                    context.scene), "hash_file_name", text="Geometry: Generate Hash Filenames")

        # Normals - relevant for all types
        col.prop(bs_plugin_data.scene_get_bs_fbx_export_settings(
            context.scene), "export_normals", text="Normals")

        # Vertex Color - relevant for Outfit, Static, Furniture, Weapon, Effect
        if config in ["Outfit", "Static", "Furniture", "Weapon", "Effect"]:
            col.prop(bs_plugin_data.scene_get_bs_fbx_export_settings(
                context.scene), "export_vertex_color", text="Vertex Color")

        # Weights - relevant for Skin, Anim, Outfit, Weapon, Door (if complex)
        if config in ["Skin", "Anim", "Outfit", "Weapon", "Door"]:
            col.prop(bs_plugin_data.scene_get_bs_fbx_export_settings(
                context.scene), "export_weights", text="Weights")

        # Morph Data - relevant for Skin, Anim, Outfit, Static (for LODs)
        if config in ["Skin", "Anim", "Outfit", "Static"]:
            col.prop(bs_plugin_data.scene_get_bs_fbx_export_settings(
                context.scene), "export_morph_data", text="Morph Data")

            # Morph Data sub-settings
            if bs_plugin_data.scene_get_bs_fbx_export_settings(context.scene).export_morph_data:
                sub_col = col.column(align=True)
                sub_col.operator(bs_plugin_data.bl_id_with_project_suffix("bgs_starfield.advanced_morph_edit"),
                               text="Advanced Morph Edit", icon='SHAPEKEY_DATA')

        # Animation Settings - relevant for Anim, Skin, Door, Container, Furniture, Weapon
        if config in ["Anim", "Skin", "Door", "Container", "Furniture", "Weapon"]:
            anim_box = layout.box()
            anim_box.label(text="Animation Settings", icon='ANIM')
            anim_col = anim_box.column(align=True)
            anim_col.prop(bs_plugin_data.scene_get_bs_fbx_export_settings(
                context.scene), "export_animations", text="Export Animations")

        # Static Mesh Settings - relevant for Static
        if config == "Static":
            static_box = layout.box()
            static_box.label(text="Static Mesh Settings", icon='MESH_CUBE')
            static_col = static_box.column(align=True)
            static_col.prop(bs_plugin_data.scene_get_bs_fbx_export_settings(
                context.scene), "apply_modifiers", text="Apply Modifiers")

        # Integrate remaining NIF settings into existing Export sections
        # NIF Template (keeps the template visible alongside other export settings)
        col_settings = settings_box.column(align=True)
        col_settings.prop(bs_plugin_data.scene_get_bs_fbx_export_settings(
            context.scene), "nif_export_template", text="NIF Template")

        # Integrate NIF-specific datatypes and controls into Export Datatypes
        # Note: Internal vs External geometry unified; no internal option in panel
        col.prop(bs_plugin_data.scene_get_bs_fbx_export_settings(
            context.scene), "nif_is_head_object", text="Head Object (NIF)")
        col.prop(bs_plugin_data.scene_get_bs_fbx_export_settings(
            context.scene), "nif_use_secondary_uv", text="Secondary UV (NIF)")

        # Snapping controls for NIF (integrated inline)
        col.prop(bs_plugin_data.scene_get_bs_fbx_export_settings(
            context.scene), "nif_snapping_enabled", text="Snapping (NIF)")
        snap_sub = col.column(align=True)
        snap_sub.prop(bs_plugin_data.scene_get_bs_fbx_export_settings(
            context.scene), "nif_snapping_range", text="Range")
        snap_sub.prop(bs_plugin_data.scene_get_bs_fbx_export_settings(
            context.scene), "nif_snap_lerp_coeff", text="Lerp Coeff")
        snap_sub.enabled = bs_plugin_data.scene_get_bs_fbx_export_settings(context.scene).nif_snapping_enabled

        # Additive export options integrated (use 'Selected Objects Only' instead of separate Base NIF control)
        # Overwrite materials and export material moved into Materials group below

        # Materials settings (moved from NIF section)
        mat_box = layout.box()
        mat_box.label(text="Materials", icon='MATERIAL')
        mat_col = mat_box.column(align=True)
        mat_col.prop(bs_plugin_data.scene_get_bs_fbx_export_settings(
            context.scene), "nif_export_material", text="Export Material (NIF)")
        mat_col.prop(bs_plugin_data.scene_get_bs_fbx_export_settings(
            context.scene), "nif_overwrite_material_paths", text="Overwrite Materials")

        # Quick Actions Section
        actions_box = layout.box()
        actions_box.label(text="Quick Actions", icon='TOOL_SETTINGS')

        actions_col = actions_box.column(align=True)
        actions_row = actions_col.row(align=True)
        actions_row.operator(bs_plugin_data.bl_id_with_project_suffix("bgs_starfield.set_recommended_unit_scale"),
                           text="Set Recommended Scale", icon='TOOL_SETTINGS')
        actions_row.operator(bs_plugin_data.bl_id_with_project_suffix("bgs_starfield.validate_scene"),
                           text="Validate Scene", icon='CHECKMARK')

        # Export Presets
        preset_box = layout.box()
        preset_box.label(text="Presets", icon='PRESET')

        preset_col = preset_box.column(align=True)
        preset_row = preset_col.row(align=True)
        preset_row.operator(bs_plugin_data.bl_id_with_project_suffix("bgs_starfield.load_preset"), text="Load Preset")
        preset_row.operator(bs_plugin_data.bl_id_with_project_suffix("bgs_starfield.save_preset"), text="Save Preset")

        # Export Buttons Section
        export_box = layout.box()
        export_box.label(text="Export", icon='EXPORT')

        export_col = export_box.column(align=True)
        
        # BSFBX Export - always available
        export_col.operator(bs_plugin_data.bl_id_with_project_suffix("bgs_starfield.verify_scene_data_and_do_export"),
                           text="Export BSFBX", icon='EXPORT')
        
        # NIF Export - always available
        export_col.operator("export_scene.custom_nif", text="Export NIF", icon='FILE')
        
        # Mesh Export - available when the export flow supports geometry
        export_col.operator("export_scene.custom_mesh", text="Export Mesh", icon='MESH_DATA')
        
        # Morph Export - show when morph data is enabled
        if bs_plugin_data.scene_get_bs_fbx_export_settings(context.scene).export_morph_data:
            export_col.operator("export_scene.custom_morph", text="Export Morph", icon='SHAPEKEY_DATA')


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
            context.scene, "bgs_starfield_active_tab", expand=True)

        if context.scene.bgs_starfield_active_tab == 'object':
            VIEW3D_PT_bgs_starfield_general.draw(self, context)
        elif context.scene.bgs_starfield_active_tab == 'collision':
            VIEW3D_PT_bgs_starfield_collision.draw(self, context)
        elif context.scene.bgs_starfield_active_tab == 'animation':
            VIEW3D_PT_bgs_starfield_animation.draw(self, context)
        elif context.scene.bgs_starfield_active_tab == 'export':
            if context.mode != 'OBJECT':
                layout.label(text="Exit Edit Mode to change settings")
                return
            VIEW3D_PT_bgs_starfield_export.draw(self, context)


def register():
    bpy.utils.register_class(VIEW3D_PT_bgs_starfield)

def unregister():
    bpy.utils.unregister_class(VIEW3D_PT_bgs_starfield)
