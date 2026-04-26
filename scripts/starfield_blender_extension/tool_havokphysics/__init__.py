# ***** BEGIN GPL LICENSE BLOCK *****
#
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.	See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ***** END GPL LICENCE BLOCK *****

# Adapted from Bethesda Game Studios' Starfield Art Tools for 3dsMax
# Copyright (C) Bethesda Game Studios

import bpy
from .ui.panels import HavokPhysicsPanel
from .ui.properties import HavokExportProperties
from .operators.export_ops import ExportVertexGroupWeightsOperator, SaveHKXSelectionSetOperator, ExportFBXAndRunImporterOperator, PostProcessHKXOperator
from .operators.util_ops import SelectVerticesFromFileOperator, OpenSelectionSetFolderOperator, SelectAbsDirPathBrowserOperator

classes = [
    HavokPhysicsPanel,
    HavokExportProperties,
    ExportVertexGroupWeightsOperator,
    SelectVerticesFromFileOperator,
    SaveHKXSelectionSetOperator,
    OpenSelectionSetFolderOperator,
    ExportFBXAndRunImporterOperator,
    PostProcessHKXOperator,
    SelectAbsDirPathBrowserOperator
]

def register():
    print("Registering tool_havokphysics")
    # Register all classes
    for cls in classes:
        try:
            bpy.utils.register_class(cls)
        except ValueError:
            print(f"Class {cls.__name__} already registered")

    # Initialize properties
    bpy.types.Scene.hkxPhysicsExport_props = bpy.props.PointerProperty(type=HavokExportProperties)

def unregister():
    # Unregister all classes
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

    # Remove properties
    del bpy.types.Scene.hkxPhysicsExport_props