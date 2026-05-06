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
from ..utils import bs_plugin_data


class BGS_STARFIELD_PG_BSFBXExportSettings(bpy.types.PropertyGroup):
    selected_only: bpy.props.BoolProperty(
        default=False,
        name="Selected Only",
        description="When TRUE, only export root_objects related to the current selection, otherwise export EVERY root object in this scene."
    )  # type: ignore
    show_additional_settings: bpy.props.BoolProperty(
        default=False,
        name="Show Additional Settings",
    )  # type: ignore
    starfield_export_scale: bpy.props.FloatProperty(
        default=40.0,
        name="Starfield Export Scale",
        description="Export scale factor for Starfield assets (default at recommended scale is 40)",
    )  # type: ignore
    export_centered_at_origin: bpy.props.BoolProperty(
        default=True,
        name="Export Centered At Origin",
        description="Export centered at origin.",
    )  # type: ignore
    export_animations: bpy.props.BoolProperty(
        default=True,
        name="Export Animations",
        description="Include animation data in export",
    )  # type: ignore
    apply_modifiers: bpy.props.BoolProperty(
        default=True,
        name="Apply Modifiers",
        description="Apply mesh modifiers during export",
    )  # type: ignore

    # New properties for the redesigned export panel
    export_directory: bpy.props.StringProperty(
        default="",
        name="Export Directory",
        description="Directory where exported files will be saved",
        subtype='DIR_PATH'
    )  # type: ignore
    compression_border: bpy.props.FloatProperty(
        default=0.0,
        name="Compression Border",
        description="Compression border setting for mesh optimization",
        min=0.0,
        max=1.0
    )  # type: ignore
    external_geometry: bpy.props.BoolProperty(
        default=False,
        name="External Geometry",
        description="Export geometry data as external .mesh files instead of embedding into the NIF"
    )  # type: ignore
    hash_file_name: bpy.props.BoolProperty(
        default=True,
        name="Geometry: Generate Hashed Filenames",
        description="Use hashed file names for external geometry files"
    )  # type: ignore
    external_geometry_export_directory: bpy.props.StringProperty(
        default="",
        name="External Geometry Export Directory",
        description="Directory for external geometry files (overrides Export Directory when set)",
        subtype='DIR_PATH'
    )  # type: ignore
    export_normals: bpy.props.BoolProperty(
        default=True,
        name="Normals",
        description="Export vertex normals"
    )  # type: ignore
    export_vertex_color: bpy.props.BoolProperty(
        default=False,
        name="Vertex Color",
        description="Export vertex color data"
    )  # type: ignore
    export_weights: bpy.props.BoolProperty(
        default=True,
        name="Weights",
        description="Export bone weight data"
    )  # type: ignore
    export_morph_data: bpy.props.BoolProperty(
        default=False,
        name="Morph Data",
        description="Export morph target data"
    )  # type: ignore

    # Morph Export Settings
    morph_use_secondary_uv: bpy.props.BoolProperty(
        name="Use Secondary UV (Morph)",
        description="Use the topmost non-active UV map (if possible) as secondary UV for morph export",
        default=False
    )  # type: ignore
    morph_snapping_enabled: bpy.props.BoolProperty(
        name="Snap Morph Data",
        description="Enable snapping morph data to nearby verts from selected objects",
        default=False
    )  # type: ignore
    morph_snapping_range: bpy.props.FloatProperty(
        name="Morph Snapping Range",
        description="Range for morph snapping",
        default=0.005,
        min=0.0,
        precision=4,
    )  # type: ignore
    morph_snap_lerp_coeff: bpy.props.FloatProperty(
        name="Morph Snap Lerp",
        description="Lerp coefficient for morph snapping",
        default=1.0,
        min=0.0,
        max=1.0,
        precision=4,
    )  # type: ignore
    morph_snap_delta_positions: bpy.props.BoolProperty(
        name="Snap Delta Positions",
        description="Also snap morph delta positions",
        default=False,
    )  # type: ignore
    morph_snap_lerp_coeff_delta_positions: bpy.props.FloatProperty(
        name="Morph Delta Lerp",
        description="Lerp for delta positions",
        default=1.0,
        min=0.0,
        max=1.0,
        precision=4,
    )  # type: ignore

    # NIF Export Settings
    nif_export_template: bpy.props.EnumProperty(
        name="NIF Template",
        description="",
        items=(('None', "As Is", "Export all items parented to the root node that are interpretable as Nif objects."),
               ('Auto', "Based On Root Name", "Auto select template based on the name of the root."),),
        default='None',
    )  # type: ignore
    # Note: compression border and weights are shared scene properties
    # (use `compression_border` and `export_weights`) - do not duplicate here.
    nif_use_secondary_uv: bpy.props.BoolProperty(
        name="Use Secondary UV",
        description="Use the topmost non-active UV map (if possible) as secondary UV",
        default=False
    )  # type: ignore
    nif_physics_tree: bpy.props.StringProperty(
        name="Physics Node Tree",
        description="Physics node tree to use for export",
        default="None"
    )  # type: ignore
    nif_export_material: bpy.props.BoolProperty(
        name="Export Material",
        description="Export material data to .mat",
        default=False,
    )  # type: ignore
    nif_is_head_object: bpy.props.EnumProperty(
        name="Export Head Object",
        description="If the model is a head model with facebones, nif export will export <model_name>.nif and <model_name>_facebones.nif.",
        items=(('None', "No", "Export the model as-is."),
               ('Auto', "Auto", "Export model.nif and model_facebones.nif separately if the model has facebone vertex groups."),),
        default='None',
    )  # type: ignore
    # Use shared `hash_file_name` property for hash name generation (already present)
    nif_snapping_enabled: bpy.props.BoolProperty(
        name="Snap Normals To Selected",
        description="Snapping data of connecting vertices to closest verts from selected objects.",
        default=False,
    )  # type: ignore
    nif_snapping_range: bpy.props.FloatProperty(
        name="Snapping Range",
        description="Verts from Active Object will copy data from verts from selected objects within Snapping Range.",
        default=0.005,
        min=0.0,
        precision=4,
    )  # type: ignore
    nif_snap_lerp_coeff: bpy.props.FloatProperty(
        name="Snap Lerp Coefficient",
        description="Lerp coefficient for snapping data of connecting vertices to closest verts from selected objects.",
        default=1.0,
        min=0.0,
        max=1.0,
        precision=4,
    )  # type: ignore
    nif_additive_export: bpy.props.EnumProperty(
        name="Base Nif From",
        description="Modify only the BSGeometry nodes in imported nif if the selected ExportScene node is from nif import. May raise errors if the number and names of models don't match.",
        items=(('None', "Disable", "Export the model as-is."),
               ('Selected', "Selected", "Overwrite selected file if applicable."),
               ('Root', "Root", "Overwrite nif file from Import_Nif_Path property of the root node."),),
        default='None',
    )  # type: ignore
    nif_overwrite_material_paths: bpy.props.BoolProperty(
        name="Overwrite Material Paths",
        description="Overwrite the material paths during additive export.",
        default=False,
    )  # type: ignore
    # Open-folder option removed from Export panel; keep internal defaults if needed


export_config_dict = {
    "Static": "Static meshes (buildings, furniture, props)",
    "Anim": "Animated objects with skeletal animation",
    "Skin": "Skinned meshes with bone weights",
    "Weapon": "Weapon models with attachments",
    "Outfit": "Character clothing and armor",
    "Furniture": "Interactive furniture objects",
    "Container": "Storage containers and chests",
    "Door": "Door and gate objects",
    "Light": "Light sources and fixtures",
    "Effect": "Particle effects and visual elements"
}


def export_config_enum_items(self, context):
    items = []
    for key, description in export_config_dict.items():
        items.append((key, key, description))
    return items


def late_register():
    bs_plugin_data.scene_assign_bs_fbx_export_settings(
        bpy.props.PointerProperty(type=BGS_STARFIELD_PG_BSFBXExportSettings))
    bs_plugin_data.scene_assign_export_config(
        bpy.props.EnumProperty(items=export_config_enum_items))


def register():
    bpy.utils.register_class(BGS_STARFIELD_PG_BSFBXExportSettings)
    late_register()

def unregister():
    bpy.utils.unregister_class(BGS_STARFIELD_PG_BSFBXExportSettings)
