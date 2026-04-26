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


class BGS_STARFIELD_PG_armature_bone_prop(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty(default="")  # type: ignore
    sgo_keep: bpy.props.BoolProperty(default=False)  # type: ignore


class BGS_STARFIELD_PG_armature_props(bpy.types.PropertyGroup):
    armature_bone_properties: bpy.props.CollectionProperty(
        type=BGS_STARFIELD_PG_armature_bone_prop)  # type: ignore


def late_register():
    bs_plugin_data.armature_assign_bgs_props(
        bpy.props.PointerProperty(type=BGS_STARFIELD_PG_armature_props))


def register():
    bpy.utils.register_class(BGS_STARFIELD_PG_armature_bone_prop)
    bpy.utils.register_class(BGS_STARFIELD_PG_armature_props)
    late_register()

def unregister():
    bpy.utils.unregister_class(BGS_STARFIELD_PG_armature_bone_prop)
    bpy.utils.unregister_class(BGS_STARFIELD_PG_armature_props)
