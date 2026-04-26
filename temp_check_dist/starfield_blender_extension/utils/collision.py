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

from .. import utils
from ..utils import bs_plugin_data

# in io_scene_bsfbx_starfield, this is in bsutil.py


def get_rigidbody_children_recursive(obj, root_obj, children=None):
    '''Recursively gather children until there are none left and return the collection in a list'''
    if children is None:
        children = []

    if obj is None:
        return children

    try:
        # do not add children of other rigidbodies
        if obj != root_obj and bs_plugin_data.object_get_bgs_rigidbody(obj).is_rigidbody:
            return children
    finally:
        pass

    if obj not in children:
        children.append(obj)

    try:
        if not obj.children:
            return children
    except ReferenceError:
        # this object was removed before StructRNA was updated, just skip it
        return children

    for child in obj.children:
        children = get_rigidbody_children_recursive(child, root_obj, children)

    return children


def get_collider_children(obj):
    rtv = []
    for o in get_rigidbody_children_recursive(obj, obj):
        if bs_plugin_data.object_get_bgs_collider(o).is_collider:
            rtv.append(o)
    return rtv
