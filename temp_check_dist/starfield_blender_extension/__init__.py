import bpy
import os
import sys

dir = os.path.dirname(os.path.realpath(__file__))
if dir not in sys.path:
	sys.path.append(dir)

from .utils import utils_common as utils

# Modules
from .ui import PhysicsPanel, MaterialPanel, BoneRegionsPanel, MorphPanel
from .operators import ImportSkeleOp, BoneRegionsOperator, NifIOOperators, MorphIOOperators, MeshIOOperators, CapsuleGenGeoNode, MaterialGenShaderNode, PlaneGenGeoNode
from . import Preferences

# StarfieldArtTools modules
from .ui import general_panel, object_panel, collision_panel, material_panel, vertex_group_panel, animation_panel, view3d_panel
from .operators import armature_ops, collision_ops, export_ops, material_ops, vertex_group_ops
from .types import object_types, armature_types, collision_types, export_types, material_types, animation_types, ui_types
from .utils import bgs, bs_plugin_data

# Havok physics tool
from . import tool_havokphysics

bl_info = {
	"name": "Starfield Blender Extension",
	"author": "SesamePaste, Deveris, and Bethesda Game Studios",
	"version": (1, 6, 0),
	"blender": (5, 0, 0),
	"location": "Sidebar > BGS Starfield Tools",
	"description": "Comprehensive suite of tools for authoring Starfield art content including mesh conversion, physics, materials, collisions, and export.",
	"warning": "",
	"category": "BGS Starfield",
}

def path_update_func(self, context):
	utils.export_mesh_folder_path = context.scene.export_mesh_folder_path
	utils.assets_folder = context.scene.assets_folder
	utils.save("cached_paths", 'export_mesh_folder_path', 'assets_folder')

utils.load("cached_paths")

__scene_global_attrs__ = {
	"sgb_debug_mode": utils.__prop_wrapper(
		bpy.props.BoolProperty,
		name="Debug Mode",
		description="Debug option. DO NOT USE.",
		default=False
	),
	"geometry_bridge_version": utils.__prop_wrapper(
		bpy.props.StringProperty,
		name="__geometry_bridge_version__",
		default = f"{bl_info['version'][0]}.{bl_info['version'][1]}.{bl_info['version'][2]}",
	),
	"export_mesh_folder_path": utils.__prop_wrapper(
		bpy.props.StringProperty,
		name="Export Folder",
		subtype='DIR_PATH',
		default= utils.export_mesh_folder_path,
		update = path_update_func
	),
	"assets_folder": utils.__prop_wrapper(
		bpy.props.StringProperty,
		name="Assets Folder",
		subtype='DIR_PATH',
		default="",
		update = path_update_func
	),
	"bgs_starfield_active_tab": utils.__prop_wrapper(
		bpy.props.EnumProperty,
		name="Active Tab",
		items=[
			('object', "General", ""),
			('collision', "Collision", ""),
			('animation', "Animation", ""),
			('export', "Export", ""),
		],
		default='object'
	),
	"br_face_type": utils.__prop_wrapper(
		bpy.props.EnumProperty,
		name="Face Type",
		items=[
			('male', "Male", ""),
			('female', "Female", ""),
		],
		default='male'
	),
	"br_driven_armature": utils.__prop_wrapper(
		bpy.props.PointerProperty,
		name="Driven Armature",
		type=bpy.types.Object,
		poll=lambda self, obj: obj.type == 'ARMATURE'
	),
}

__modules__ = [
	PhysicsPanel,
	MaterialPanel,
	ImportSkeleOp,
	Preferences,
	BoneRegionsOperator,
	BoneRegionsPanel,
	MorphPanel,
	MeshIOOperators,
	MorphIOOperators,
	NifIOOperators,
	# StarfieldArtTools modules
	general_panel,
	collision_panel,
	material_panel,
	vertex_group_panel,
	animation_panel,
	view3d_panel,
	armature_ops,
	collision_ops,
	export_ops,
	material_ops,
	vertex_group_ops,
	object_types,
	armature_types,
	collision_types,
	export_types,
	material_types,
	animation_types,
	ui_types,
	tool_havokphysics,
]

# Register the operators and menu entries
def register():
	print("Registering Starfield Blender Extension")

	for attr in __scene_global_attrs__:
		setattr(bpy.types.Scene, attr, __scene_global_attrs__[attr]())
	
	for module in __modules__:
		if hasattr(module, 'register'):
			print(f"Registering module: {module}")
			module.register()
	
	# StarfieldArtTools preferences are unified in Preferences.SGBPreferences.

def unregister():

	for attr in __scene_global_attrs__:
		delattr(bpy.types.Scene, attr)

	for module in __modules__:
		if hasattr(module, 'unregister'):
			module.unregister()
	
	# StarfieldArtTools preferences are unified in Preferences.SGBPreferences.

if __name__ == "__main__":
	register()