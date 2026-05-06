import bpy
import os

from .. import MeshIO, MorphIO

from ..utils import utils_blender, utils_common as utils
from ..utils import bs_plugin_data

# Export operator
class ExportCustomMesh(bpy.types.Operator):
	bl_idname = "export_scene.custom_mesh"
	bl_label = "Export Custom Mesh"
	bl_description = "Export mesh data in Starfield .mesh format for external geometry"
	
	filepath: bpy.props.StringProperty(options={'HIDDEN'})
	filename: bpy.props.StringProperty(default='untitled.mesh')
	filter_glob: bpy.props.StringProperty(default="*.mesh", options={'HIDDEN'})
	
	max_border: bpy.props.FloatProperty(
		name="Compression Border",
		description="2 for body parts, 0 otherwise.",
		default=0,
	)
	use_world_origin: bpy.props.BoolProperty(
		name="Use world origin",
		description="Use world instead of object origin as output geometry's origin.",
		default=True
	)
	WEIGHTS: bpy.props.BoolProperty(
		name="Weights",
		description="Export vertex weights, only work with valid armature modifiers attached to objects.",
		default=True
	)
	use_secondary_uv: bpy.props.BoolProperty(
		name="Use Secondary UV",
		description="Use the topmost non-active UV map (if possible) as secondary UV",
		default=False
	)

	export_morph: bpy.props.BoolProperty(
		name="Export morph data (if any)",
		description="Export shape keys as morph keys",
		default=False,
	)

	export_sf_mesh_open_folder: bpy.props.BoolProperty(
		name="Open folder after export",
		default=False,
	)
	export_sf_mesh_hash_result: bpy.props.BoolProperty(
		name="Generate hash names",
		description="Export into [hex1]\\[hex2].mesh instead of [name].mesh",
		default=False,
	)

	snapping_enabled: bpy.props.BoolProperty(
		name="Snap Normals To Selected",
		description="Snapping data of connecting vertices to closest verts from selected objects.",
		default=False,
	)

	snap_lerp_coeff: bpy.props.FloatProperty(
		name="Snap Lerp Coefficient",
		description="Lerp coefficient for snapping data of connecting vertices to closest verts from selected objects.",
		default=1.0,
		min=0.0,
		max=1.0,
		precision=4,
	)

	snapping_range: bpy.props.FloatProperty(
		name="Snapping Range",
		description="Verts from Active Object will copy data from verts from selected objects within Snapping Range.",
		default=0.005,
		min=0.0,
		precision=4,
	)

	def draw(self, context):
		layout = self.layout

		layout.prop(self, "max_border")

		layout.separator()
		layout.prop(self, "use_world_origin")
		layout.prop(self, "WEIGHTS")
		layout.prop(self, "use_secondary_uv")

		report = utils_blender.export_report(report_uv_layers=True)
		box = layout.box()
		if self.use_secondary_uv:
			box.label(text=f"First UV Map: {report['first_uv'].name}")
			box.label(text=f"Second UV Map: {report['second_uv'].name}")
		else:
			box.label(text=f"UV Map: {report['first_uv'].name}")

		layout.prop(self, "export_sf_mesh_hash_result")

		layout.separator()
		layout.label(text="Snapping data:") 
		layout.prop(self, "snapping_enabled")

		box = layout.box()

		box.prop(self, "snapping_range")
		box.prop(self, "snap_lerp_coeff")
		box_row = box.row()

		box_row.enabled = False
		box.enabled = False
		if self.snapping_enabled:
			box.enabled = True
		
		layout.separator()
		layout.label(text="After Export:") 
		layout.prop(self, "export_morph")
		layout.prop(self, "export_sf_mesh_open_folder")

	def execute(self,context):
		_try_import_success, _rtn_str = utils._try_import("import scipy", "Scipy not installed. Install it in Plugin Preferences Panel.", raise_exception=False)
		if not _try_import_success:
			self.report({'ERROR'}, _rtn_str)
			return {'CANCELLED'}

		# Persist any changes made in the file browser back to scene settings
		settings = bs_plugin_data.scene_get_bs_fbx_export_settings(context.scene)
		settings.compression_border = self.max_border
		settings.export_morph_data = self.export_morph
		settings.hash_file_name = self.export_sf_mesh_hash_result
		
		original_active = utils_blender.GetActiveObject()
		original_selected = utils_blender.GetSelectedObjs(True)

		if self.snapping_enabled:
			mesh_success, _, _, _ = MeshIO.ExportMesh(self,context,self.filepath,self, ref_objects=original_selected)
		else:
			mesh_success, _, _, _ = MeshIO.ExportMesh(self,context,self.filepath,self)

		if 'FINISHED' in mesh_success and self.export_morph:
			utils_blender.SetSelectObjects(original_selected)
			utils_blender.SetActiveObject(original_active)
			_file_name, _ =os.path.splitext(self.filepath)
			morph_success, _ = MorphIO.ExportMorph_alt(self,context, _file_name + ".dat", self)
			if 'FINISHED' in morph_success:
				self.report({'INFO'}, "Operation successful.")

			return morph_success
		
		return mesh_success

	def invoke(self, context, event):
		# Sync operator properties with scene settings
		settings = bs_plugin_data.scene_get_bs_fbx_export_settings(context.scene)
		self.max_border = settings.compression_border
		self.export_morph = settings.export_morph_data
		self.export_sf_mesh_hash_result = settings.hash_file_name

		_obj = context.active_object
		if _obj:
			self.filename = utils.sanitize_filename(_obj.name) + '.mesh'
		else:
			self.filename = 'untitled.mesh'

		# Prefer the external geometry export directory if set, otherwise fall
		# back to the global export_directory. This ensures the file browser
		# opens where the user configured external geometry to be written.
		export_dir = None
		try:
			export_dir = settings.external_geometry_export_directory
		except Exception:
			export_dir = None

		if not export_dir:
			# fallback to general export directory
			export_dir = getattr(settings, 'export_directory', None)

		if export_dir:
			export_dir = os.path.expanduser(os.path.expandvars(export_dir))
			if os.path.isdir(export_dir):
				# Set filepath and perform export immediately without showing
				# a file browser.
				self.filepath = os.path.join(export_dir, self.filename)
				# Call execute directly to perform the export
				return self.execute(context)
			else:
				# If the configured path doesn't exist, fall back to file browser
				pass

		# No export directory configured -> prompt user with file browser
		context.window_manager.fileselect_add(self)
		return {'RUNNING_MODAL'}

# Import operator
class ImportCustomMesh(bpy.types.Operator):
	bl_idname = "import_scene.custom_mesh"
	bl_label = "Import Custom Mesh"
	
	filepath: bpy.props.StringProperty(subtype="FILE_PATH")
	filename: bpy.props.StringProperty(default='untitled.mesh')
	
	filter_glob: bpy.props.StringProperty(default="*.mesh", options={'HIDDEN'})

	def assets_folder_update(self, context):
		context.scene.assets_folder = self.assets_folder

	assets_folder: bpy.props.StringProperty(subtype="FILE_PATH", update=assets_folder_update)

	import_as_read_only: bpy.props.BoolProperty(
		name="As Read Only",
		description="The object will be marked as read only. You can import morph once, however, as long as there's morph data in this object, any attempt to import a new morph will be prohibited.",
		default=False
	)
	meshlets_debug: bpy.props.BoolProperty(
		name="Debug Meshlets",
		description="Debug option. DO NOT USE.",
		default=False
	)
	culldata_debug: bpy.props.BoolProperty(
		name="Debug CullData",
		description="Debug option. DO NOT USE.",
		default=False
	)
	tangents_debug: bpy.props.BoolProperty(
		name="Debug Tangent Vectors",
		description="Debug option. DO NOT USE.",
		default=False
	)

	def execute(self, context):
		return MeshIO.ImportMesh_Alt(self.filepath, self, context, self)

	def invoke(self, context, event):
		self.assets_folder = context.scene.assets_folder
		context.window_manager.fileselect_add(self)
		return {'RUNNING_MODAL'}

	def draw(self, context):
		layout = self.layout
		layout.label(text="Assets Folder:")
		layout.prop(self, "assets_folder", text="")

__classes__ = [
	ExportCustomMesh,
    ImportCustomMesh,
]

# Add custom menu entries in the File menu
def menu_func_export(self, context):
	self.layout.operator(
		ExportCustomMesh.bl_idname,
		text="Starfield Geometry (.mesh)",
	)

def menu_func_import(self, context):
	self.layout.operator(
		ImportCustomMesh.bl_idname,
		text="Starfield Geometry (.mesh)",
	)

def register():
    for c in __classes__:
        bpy.utils.register_class(c)
        
    bpy.types.TOPBAR_MT_file_export.append(menu_func_export)
    bpy.types.TOPBAR_MT_file_import.append(menu_func_import)
		
def unregister():
    for c in __classes__:
        bpy.utils.unregister_class(c)
        
    bpy.types.TOPBAR_MT_file_export.remove(menu_func_export)
    bpy.types.TOPBAR_MT_file_import.remove(menu_func_import)
