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

from .. import utils

# CALLBACKS


def bgs_panel_tab_items(self, context):
    items = [
        ("OBJECT", "General", ""),
        ("COLLISION", "Collision", ""),
        ("ANIMATION", "Animation", ""),
        ("EXPORT", "Export", ""),
    ]
    return items


bs_plugin_data.scene_assign_bgs_starfield_panel_tab(
    bpy.props.EnumProperty(items=bgs_panel_tab_items))


def register():
    bs_plugin_data.scene_assign_bgs_starfield_panel_tab(bpy.props.EnumProperty(items=bgs_panel_tab_items))

def unregister():
    pass
