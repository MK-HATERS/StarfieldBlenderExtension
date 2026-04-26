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
from bpy import props, types
from ..utils import bgs
from ..utils import bs_plugin_data

alpha_function_types = {
    "ALPHA_ONE": 0,
    "ALPHA_ZERO": 1,
    "ALPHA_SRCCOLOR": 2,
    "ALPHA_INVSRCCOLOR": 3,
    "ALPHA_DESTCOLOR": 4,
    "ALPHA_INVDESTCOLOR": 5,
    "ALPHA_SRCALPHA": 6,
    "ALPHA_INVSRCALPHA": 7,
    "ALPHA_DESTALPHA": 8,
    "ALPHA_INVDESTALPHA": 9,
    "ALPHA_SRCALPHASAT": 10,
}


def alpha_function_type_items(self, context):
    items = []
    for k, v in alpha_function_types.items():
        items.append((str(v), k, ''))
    return items


class BGS_STARFIELD_PG_material_properties(bpy.types.PropertyGroup):
    material_type: bpy.props.EnumProperty(
        name="Material Type",
        items=[
            ("LIGHTING", "Lighting", "Lighting Material (Default)"),
            ("EFFECT", "Effect", "Effect Material"),
        ],
        default="LIGHTING"
    )  # type: ignore[reportInvalidTypeForm]

    clamp_mode: bpy.props.EnumProperty(  # TODO: ui
        name="Clamp Mode",
        items=[
            ("CLAMP_S_CLAMP_T", "TEXTURE_ADDRESS_MODE_CLAMP_S_CLAMP_T", ""),
            ("CLAMP_S_WRAP_T", "TEXTURE_ADDRESS_MODE_CLAMP_S_WRAP_T", ""),
            ("WRAP_S_CLAMP_T", "TEXTURE_ADDRESS_MODE_WRAP_S_CLAMP_T", ""),
            ("WRAP_S_WRAP_T", "TEXTURE_ADDRESS_MODE_WRAP_S_WRAP_T", ""),
            ("BORDER", "TEXTURE_ADDRESS_MODE_BORDER", ""),
            ("MIRROR", "TEXTURE_ADDRESS_MODE_MIRROR", ""),
        ],
        default="WRAP_S_WRAP_T"
    )  # type: ignore

    show_additional_texture_settings: bpy.props.BoolProperty(default=False)  # type: ignore

    texture_diffuse: bpy.props.StringProperty(
        default="textures\\default.dds"
    )  # TEXTYPE_DIFFUSE = 0  # type: ignore
    texture_normal: bpy.props.StringProperty(
        default="textures\\default_n.dds"
    )  # TEXTYPE_NORMAL/TEXTYPE_GLOSS = 1 # type: ignore
    texture_glow: bpy.props.StringProperty(
        default=""
    )  # TEXTYPE_GLOW/TEXTYPE_SKIN_SST/TEXTYPE_HAIR_LAYER = 2 # type: ignore
    texture_height: bpy.props.StringProperty(
        default=""
    )  # TEXTYPE_HEIGHT/TEXTYPE_FG_DETAIL = 3 # type: ignore
    texture_environment: bpy.props.StringProperty(
        default=""
    )  # TEXTYPE_ENV = 4  # type: ignore
    texture_environment_mask: bpy.props.StringProperty(
        default=""
    )  # TEXTYPE_ENV_MASK = 5  # type: ignore
    texture_multilayer: bpy.props.StringProperty(
        default=""
    )  # TEXTYPE_MULTILAYER/TEXTYPE_FG_TINT = 6  # type: ignore
    texture_backlight_mask: bpy.props.StringProperty(
        default=""
    )  # TEXTYPE_BACKLIGHT_MASK = 7  # type: ignore
    texture_noise: bpy.props.StringProperty(
        default=""
    )  # TEXTYPE_NOISE = 8 # type: ignore

    # ----- UV Settings -----
    show_uv_settings: bpy.props.BoolProperty(default=False)  # type: ignore
    uvoffset: bpy.props.FloatVectorProperty(
        default=(0.0, 0.0), size=2
    )  # type: ignore
    uvscale: bpy.props.FloatVectorProperty(
        default=(1.0, 1.0), size=2
    )  # type: ignore

    # ----- Environment Mapping -----
    environment_mapping: bpy.props.BoolProperty(default=False)  # type: ignore
    environment_mapping_scale: bpy.props.FloatProperty(
        default=1.0
    )  # type: ignore

    show_additional_material_settings: bpy.props.BoolProperty(
        default=False
    )  # type: ignore

    # ----- Alpha -----
    alpha_enabled: bpy.props.BoolProperty(default=False)  # type: ignore
    material_alpha: bpy.props.FloatProperty(default=1.0)  # type: ignore
    alpha_ref: bpy.props.IntProperty(default=0)  # type: ignore
    alpha_mode: bpy.props.EnumProperty(
        name="Alpha Mode",
        items=[
            ('1', "Standard", ""),
            ('2', "Additive", ""),
            ('3', "Multiplicative", ""),
            ('4', "None", ""),
            (str(bgs.custom_enum_value()), "Custom", ""),
        ],
        default="1"
    )  # type: ignore

    custom_alpha_blend: bpy.props.BoolProperty(
        default=True, name="Custom Alpha Enabled")  # type: ignore
    custom_alpha_src_blend_mode: bpy.props.EnumProperty(
        items=alpha_function_type_items, default=2, name="Src Blend Mode")  # type: ignore
    custom_alpha_dest_blend_mode: bpy.props.EnumProperty(
        items=alpha_function_type_items, default=3, name="Dest Blend Mode")  # type: ignore

    # ----- SetupDataLightingShader -----
    refraction: bpy.props.BoolProperty(default=False)  # type: ignore
    refraction_power: bpy.props.FloatProperty(default=0.0)  # type: ignore
    refraction_falloff: bpy.props.BoolProperty(default=False)  # type: ignore

    back_lighting: bpy.props.BoolProperty(default=False)  # type: ignore
    sub_surface_lighting: bpy.props.BoolProperty(default=False)  # type: ignore
    rim_lighting: bpy.props.BoolProperty(default=False)  # type: ignore
    subsurface_rolloff: bpy.props.FloatProperty(default=0.0)  # type: ignore
    rim_power: bpy.props.FloatProperty(default=0.0)  # type: ignore
    aniso_lighting: bpy.props.BoolProperty(default=False)  # type: ignore

    emit_color: bpy.props.FloatVectorProperty(
        subtype="COLOR",
        default=(0.0, 0.0, 0.0),
        min=0.0,
        max=1.0,
    )  # type: ignore
    emit_color_scale: bpy.props.FloatProperty(default=1.0)  # type: ignore

    shininess: bpy.props.FloatProperty(default=80.0)  # type: ignore
    specular_enabled: bpy.props.BoolProperty(default=True)  # type: ignore
    specular_mult: bpy.props.FloatProperty(default=1.0)  # type: ignore
    specular_color: bpy.props.FloatVectorProperty(
        subtype="COLOR",
        default=(1.0, 1.0, 1.0),
        min=0.0,
        max=1.0,
    )  # type: ignore
    has_custom_specular_color: bpy.props.BoolProperty(default=False)  # type: ignore
    custom_specular_color: bpy.props.FloatVectorProperty(
        default=(1.0, 1.0, 1.0),
    )  # type: ignore

    # ----- SetupEffectShaderProperty -----

    falloff_enabled: bpy.props.BoolProperty(default=False)  # type: ignore
    falloff_start_angle: bpy.props.FloatProperty(
        default=0.0, min=0.0, max=360.0)  # type: ignore
    falloff_stop_angle: bpy.props.FloatProperty(
        default=0.0, min=0.0, max=360.0)  # type: ignore
    falloff_start_opacity: bpy.props.FloatProperty(
        default=0.0, min=0.0, max=360.0)  # type: ignore
    falloff_stop_opacity: bpy.props.FloatProperty(
        default=0.0, min=0.0, max=360.0)  # type: ignore

    lighting_influence: bpy.props.FloatProperty(default=1.0)  # type: ignore

    soft_enabled: bpy.props.BoolProperty(default=False)  # type: ignore
    soft_falloff_depth: bpy.props.FloatProperty(default=100.0)  # type: ignore

    # ----- Flags -----

    show_additional_material_flags: bpy.props.BoolProperty(default=False)  # type: ignore

    vertex_colors_enabled: bpy.props.BoolProperty(
        default=True)  # bVertexColors # type: ignore
    vertex_alpha_enabled: bpy.props.BoolProperty(default=False)  # bVertexAlpha # type: ignore
    face_gen: bpy.props.BoolProperty(default=False)  # bFacegen # type: ignore
    parallax_enabled: bpy.props.BoolProperty(default=False)  # bParallax # type: ignore
    parallax_occlusion_enabled: bpy.props.BoolProperty(
        default=False)  # bParallaxOcclusion # type: ignore
    model_space_normals: bpy.props.BoolProperty(
        default=False)  # bModelSpaceNormals # type: ignore
    hair: bpy.props.BoolProperty(default=False)  # bHair # type: ignore
    remappable_textures: bpy.props.BoolProperty(
        default=True)  # bRemappableTextures # type: ignore
    decal: bpy.props.BoolProperty(default=False)  # bDecal # type: ignore
    zbuffer_test: bpy.props.BoolProperty(default=True)  # bZBufferTest # type: ignore
    zbuffer_write: bpy.props.BoolProperty(default=True)  # bZBufferWrite # type: ignore
    hide_secret: bpy.props.BoolProperty(default=False)  # bHideSecret # type: ignore
    no_fade: bpy.props.BoolProperty(default=False)  # bNoFade # type: ignore
    light_fade: bpy.props.BoolProperty(default=False)  # bLightFade # type: ignore
    effect_lighting_enabled: bpy.props.BoolProperty(
        default=False)  # bEffectLightingEnabled # type: ignore
    multi_layer_parallax_enabled: bpy.props.BoolProperty(
        default=False)  # bMultiLayerParallax # type: ignore
    tree: bpy.props.BoolProperty(default=False)  # bTree # type: ignore
    blood_enabled: bpy.props.BoolProperty(default=False)  # bBloodEnabled # type: ignore
    grayscale_to_palette_color: bpy.props.BoolProperty(
        default=False)  # bGrayscaleToPaletteColor # type: ignore
    grayscale_to_palette_alpha: bpy.props.BoolProperty(
        default=False)  # bGrayscaleToPaletteAlpha # type: ignore
    cast_shadows: bpy.props.BoolProperty(default=True)  # bCastShadows # type: ignore
    receive_shadows: bpy.props.BoolProperty(default=True)  # bReceiveShadows # type: ignore
    dissolve_fade: bpy.props.BoolProperty(default=False)  # bDissolveFade # type: ignore
    glowmap_enabled: bpy.props.BoolProperty(default=False)  # bGlowmap # type: ignore
    two_sided_enabled: bpy.props.BoolProperty(default=False)  # bTwoSided # type: ignore
    assume_shadowmask: bpy.props.BoolProperty(
        default=False)  # bAssumeShadowmask # type: ignore
    environment_mapping_eye: bpy.props.BoolProperty(
        default=False)  # bEnvironmentMappingEye # type: ignore
    external_emittance: bpy.props.BoolProperty(
        default=False)  # bExternalEmittance # type: ignore


def late_register():
    bs_plugin_data.material_assign_bgs_props(
        bpy.props.PointerProperty(type=BGS_STARFIELD_PG_material_properties))


def register():
    bpy.utils.register_class(BGS_STARFIELD_PG_material_properties)
    late_register()

def unregister():
    bpy.utils.unregister_class(BGS_STARFIELD_PG_material_properties)
