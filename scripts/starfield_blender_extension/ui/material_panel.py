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

# NOTE:
# This panel appears under the active object's "MATERIALS" property context.

import bpy
from bpy.props import *

from pprint import pprint

from .. import utils
from ..utils import bgs
from ..utils import bs_plugin_data


class BGS_STARFIELD_PT_object_mat_palette(bpy.types.Panel):
    bl_idname = bs_plugin_data.bl_id_with_project_suffix(
        "BGS_STARFIELD_PT_object_mat_palette")
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'HEADER'
    bl_category = 'BGS Starfield'
    bl_label = ' '

    def draw(self, context):
        if context.active_object is None:
            return
        if context.active_object.active_material is None:
            return

        layout = self.layout

        box = layout.box()
        box.label(text='BGS Material Properties (Starfield)')

        material_bgs_props = bs_plugin_data.material_get_bgs_props(
            context.active_object.active_material)
        box.prop(material_bgs_props, "material_type", text="Material Type")

        is_lighting_material = material_bgs_props.material_type == "LIGHTING"
        is_effect_material = material_bgs_props.material_type == "EFFECT"

        if is_lighting_material:
            box.prop(material_bgs_props, "texture_diffuse",
                     text="Diffuse Texture (Base)")
            box.prop(material_bgs_props, "texture_normal",
                     text="Normal Texture (Gloss)")

        elif is_effect_material:
            box.prop(material_bgs_props, "texture_diffuse",
                     text="Base Texture (Diffuse)")
            box.prop(material_bgs_props, "texture_normal",
                     text="Normal Texture (Gloss)")

        box.operator(bs_plugin_data.bl_id_with_project_suffix(
            'bgs_starfield.load_path_material'), icon='TEXTURE')

        box.prop(material_bgs_props, "show_additional_texture_settings",
                 text="Show Additional Texture Slots")
        if material_bgs_props.show_additional_texture_settings:
            box_parent = box
            box = box.box()
            box.prop(material_bgs_props, "texture_glow",
                     text="Glow Texture (Glow, Hair, Skin Subsurface Tint)")
            box.prop(material_bgs_props, "texture_height",
                     text="Height Texture (FaceGen Detail)")
            box.prop(material_bgs_props, "texture_environment",
                     text="Environment Texture")
            box.prop(material_bgs_props, "texture_environment_mask",
                     text="Environment Mask Texture")
            box.prop(material_bgs_props, "texture_multilayer",
                     text="Multilayer Texture (FaceGen Tint)")
            box.prop(material_bgs_props, "texture_backlight_mask",
                     text="Backlight Mask Texture (Skin Specular)")
            box.prop(material_bgs_props, "texture_noise", text="Noise Texture")
            box = box_parent

        box.prop(material_bgs_props, "environment_mapping",
                 text="Environment Mapping")
        if material_bgs_props.environment_mapping:
            box_parent = box
            box = box.box()
            box.prop(material_bgs_props, "environment_mapping_scale",
                     text="Scale (Environment Map)")
            box = box_parent

        box.prop(material_bgs_props, "show_uv_settings",
                 text="Show UV Settings")
        if material_bgs_props.show_uv_settings:
            box_parent = box
            box = box.box()
            box.prop(material_bgs_props, "clamp_mode", text="Clamp Mode")
            box.prop(material_bgs_props, "uvoffset", text="UV Offset")
            box.prop(material_bgs_props, "uvscale", text="UV Scale")
            box = box_parent

        box.prop(material_bgs_props, "specular_enabled",
                 text="Specular Enabled [Spc]")
        if material_bgs_props.specular_enabled:
            box_sub_parent = box
            box = box.box()
            box.prop(material_bgs_props, "specular_color",
                     text="Specular Color")
            box.prop(material_bgs_props, "has_custom_specular_color",
                     text="Has Custom Specular Color")
            if material_bgs_props.has_custom_specular_color:
                box.prop(material_bgs_props, "custom_specular_color",
                         text="Custom Specular Color")
            box.prop(material_bgs_props, "shininess", text="Shininess")
            box.prop(material_bgs_props, "specular_mult", text="Specular Mult")
            box = box_sub_parent

        box.prop(material_bgs_props, "alpha_enabled", text="Alpha Enabled")
        if material_bgs_props.alpha_enabled:
            box_sub_parent = box
            box = box.box()
            box.prop(material_bgs_props, "alpha_mode", text="Alpha Mode")
            if int(material_bgs_props.alpha_mode) == bgs.custom_enum_value():
                box.prop(material_bgs_props, "custom_alpha_blend")
                box.prop(material_bgs_props, "custom_alpha_src_blend_mode")
                box.prop(material_bgs_props, "custom_alpha_dest_blend_mode")
            box.prop(material_bgs_props, "material_alpha",
                     text="Material Alpha")
            box.prop(material_bgs_props, "alpha_ref", text="Alpha Ref")
            box = box_sub_parent

        box.prop(material_bgs_props, "show_additional_material_settings",
                 text="Show Additional Material Properties")
        if material_bgs_props.show_additional_material_settings:
            box_parent = box
            box = box.box()

            if is_lighting_material:

                box.prop(material_bgs_props, "refraction", text="Refraction")
                if material_bgs_props.refraction:
                    box_sub_parent = box
                    box = box.box()
                    box.prop(material_bgs_props, "refraction_power",
                             text="Refraction Power")
                    box.prop(material_bgs_props, "refraction_falloff",
                             text="Refraction Falloff")
                    box = box_sub_parent

                box.prop(material_bgs_props, "back_lighting",
                         text="Back Lighting [Bk]")

                box.prop(material_bgs_props, "sub_surface_lighting",
                         text="Subsurface Lighting (Soft Lighting) [Sss]")
                if material_bgs_props.sub_surface_lighting:
                    box_sub_parent = box
                    box = box.box()
                    box.prop(material_bgs_props, "subsurface_rolloff",
                             text="Subsurface Rolloff")
                    box = box_sub_parent

                box.prop(material_bgs_props, "rim_lighting",
                         text="Rim Lighting [Rim]")
                if material_bgs_props.rim_lighting:
                    box_sub_parent = box
                    box = box.box()
                    box.prop(material_bgs_props, "rim_power", text="Rim Power")
                    box = box_sub_parent
                box.prop(material_bgs_props, "aniso_lighting",
                         text="Aniso Lighting")

                box.prop(material_bgs_props, "emit_color", text="Emit Color")
                box.prop(material_bgs_props, "emit_color_scale",
                         text="Emit Color Scale")

            elif is_effect_material:
                box.prop(material_bgs_props, "falloff_enabled",
                         text="Falloff Enabled")
                if material_bgs_props.falloff_enabled:
                    box_sub_parent = box
                    box = box.box()
                    box.prop(material_bgs_props, "falloff_start_angle",
                             text="Falloff Start Angle")
                    box.prop(material_bgs_props, "falloff_stop_angle",
                             text="Falloff Stop Angle")
                    box.prop(material_bgs_props, "falloff_start_opacity",
                             text="Falloff Start Opacity")
                    box.prop(material_bgs_props, "falloff_stop_opacity",
                             text="Falloff Stop Opacity")
                    box = box_sub_parent

                box.prop(material_bgs_props, "emit_color", text="Base Color")
                box.prop(material_bgs_props, "material_alpha",
                         text="Base Color Alpha")

                box.prop(material_bgs_props, "soft_enabled",
                         text="Soft Enabled")
                if material_bgs_props.soft_enabled:
                    box_sub_parent = box
                    box = box.box()
                    box.prop(material_bgs_props, "soft_falloff_depth",
                             text="Soft Falloff Depth")
                    box = box_sub_parent

            box = box_parent

        box.prop(material_bgs_props, "show_additional_material_flags",
                 text="Show Additional Material Flags")
        if material_bgs_props.show_additional_material_flags:
            box_parent = box
            box = box.box()

            # box.prop(material_bgs_props, "vertex_colors_enabled", text="Vertex Colors [Vc]")
            box.prop(material_bgs_props, "vertex_alpha_enabled",
                     text="Vertex Alpha")
            box.prop(material_bgs_props, "face_gen", text="Facegen")
            box.prop(material_bgs_props, "parallax_enabled", text="Parallax")
            box.prop(material_bgs_props, "parallax_occlusion_enabled",
                     text="Parallax Occlusion")
            box.prop(material_bgs_props, "model_space_normals",
                     text="Model Space Normals [Msn] (May need Subsurface Lighting)")
            box.prop(material_bgs_props, "hair", text="Hair")
            box.prop(material_bgs_props, "remappable_textures",
                     text="Remappable Textures")
            box.prop(material_bgs_props, "decal", text="Decal")
            box.prop(material_bgs_props, "zbuffer_test", text="Z-Buffer Test")
            box.prop(material_bgs_props, "zbuffer_write",
                     text="Z-Buffer Write")
            box.prop(material_bgs_props, "hide_secret", text="Hide Secret")
            box.prop(material_bgs_props, "no_fade", text="No Fade")
            box.prop(material_bgs_props, "light_fade", text="Light Fade")
            box.prop(material_bgs_props, "effect_lighting_enabled",
                     text="Effect Lighting Enabled")
            box.prop(material_bgs_props, "multi_layer_parallax_enabled",
                     text="Multi-Layer Parallax")
            box.prop(material_bgs_props, "tree", text="Tree")
            box.prop(material_bgs_props, "blood_enabled", text="Blood Enabled")
            box.prop(material_bgs_props, "grayscale_to_palette_color",
                     text="Grayscale to Palette Color")
            box.prop(material_bgs_props, "grayscale_to_palette_alpha",
                     text="Grayscale to Palette Alpha")
            box.prop(material_bgs_props, "cast_shadows", text="Cast Shadows")
            box.prop(material_bgs_props, "receive_shadows",
                     text="Receive Shadows")
            box.prop(material_bgs_props, "dissolve_fade", text="Dissolve Fade")
            box.prop(material_bgs_props, "glowmap_enabled", text="Glowmap")
            box.prop(material_bgs_props, "two_sided_enabled", text="Two-Sided")
            box.prop(material_bgs_props, "assume_shadowmask",
                     text="Assume Shadowmask")
            box.prop(material_bgs_props, "environment_mapping_eye",
                     text="Environment Mapping Eye")
            box.prop(material_bgs_props, "external_emittance",
                     text="External Emittance")

            box = box_parent


class BGS_STARFIELD_PT_bgs_materials(bpy.types.Panel):
    # main object material panel override
    bl_idname = bs_plugin_data.bl_id_with_project_suffix(
        "BGS_STARFIELD_PT_bgs_materials")
    bl_space_type = 'IMAGE_EDITOR'
    bl_region_type = 'UI'
    bl_category = 'BGS Starfield'
    bl_label = "BGS"
    COMPAT_ENGINES = {'BLENDER_EEVEE', 'BLENDER_WORKBENCH'}

    blender_eevee_mat_draw = None
    blender_cycles_mat_draw = None

    @classmethod
    def poll(cls, context):
        ob = context.object
        if ob is None:
            return False
        mat = context.object.active_material

        if (ob and ob.type == 'GPENCIL') or (mat and mat.grease_pencil):
            return False

        return (ob or mat) and (context.engine in cls.COMPAT_ENGINES)

    def EEVEE_MATERIAL_PT_context_material_draw(self, context):
        BGS_STARFIELD_PT_bgs_materials.blender_eevee_mat_draw(self, context)
        BGS_STARFIELD_PT_object_mat_palette.draw(self, context)

    def CYCLES_PT_context_material_draw(self, context):
        BGS_STARFIELD_PT_bgs_materials.blender_cycles_mat_draw(self, context)
        BGS_STARFIELD_PT_object_mat_palette.draw(self, context)

    def draw(self, context):
        pass


def register_custom():
    try:
        if hasattr(bpy.types, "EEVEE_MATERIAL_PT_context_material"):
            BGS_STARFIELD_PT_bgs_materials.blender_eevee_mat_draw = bpy.types.EEVEE_MATERIAL_PT_context_material.draw
            bpy.types.EEVEE_MATERIAL_PT_context_material.draw = BGS_STARFIELD_PT_bgs_materials.EEVEE_MATERIAL_PT_context_material_draw

        if hasattr(bpy.types, "CYCLES_PT_context_material"):
            BGS_STARFIELD_PT_bgs_materials.blender_cycles_mat_draw = bpy.types.CYCLES_PT_context_material.draw
            bpy.types.CYCLES_PT_context_material.draw = BGS_STARFIELD_PT_bgs_materials.CYCLES_PT_context_material_draw
    except BaseException as e:
        print("material_panel register_custom failed(%s)" % (e))


def unregister_custom():
    # restore the original draw func
    try:
        if hasattr(bpy.types, "EEVEE_MATERIAL_PT_context_material") and BGS_STARFIELD_PT_bgs_materials.blender_eevee_mat_draw is not None:
            bpy.types.EEVEE_MATERIAL_PT_context_material.draw = BGS_STARFIELD_PT_bgs_materials.blender_eevee_mat_draw
    except BaseException as e:
        print("material_panel unregister_custom failed(%s)" % (e))

    try:
        if hasattr(bpy.types, "CYCLES_PT_context_material") and BGS_STARFIELD_PT_bgs_materials.blender_cycles_mat_draw is not None:
            bpy.types.CYCLES_PT_context_material.draw = BGS_STARFIELD_PT_bgs_materials.blender_cycles_mat_draw
    except BaseException as e:
        print("material_panel unregister_custom failed(%s)" % (e))


def register():
    bpy.utils.register_class(BGS_STARFIELD_PT_object_mat_palette)
    bpy.utils.register_class(BGS_STARFIELD_PT_bgs_materials)
    register_custom()

def unregister():
    bpy.utils.unregister_class(BGS_STARFIELD_PT_object_mat_palette)
    bpy.utils.unregister_class(BGS_STARFIELD_PT_bgs_materials)
    unregister_custom()
