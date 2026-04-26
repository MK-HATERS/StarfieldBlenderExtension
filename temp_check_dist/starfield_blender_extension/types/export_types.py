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


export_config_list = [
    "Static",
    "Anim",
    "Skin",
    "Weapon",
    "Outfit",
]


def export_config_enum_items(self, context):
    items = []
    for k in export_config_list:
        items.append((k, k, ''))
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
