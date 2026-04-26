import bpy


class HavokPhysicsPanel(bpy.types.Panel):
    bl_label = "Havok physics exporter"
    bl_idname = "VIEW3D_PT_bgs_starfield_havok"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "object"
    bl_category = "BGS Starfield"

    def draw(self, context):
        layout = self.layout
        props = context.scene.hkxPhysicsExport_props
        obj = context.active_object
        scene = context.scene

        layout.label(text="Root export folder, selection sets will be saved here. Default: this blend files' location")
        layout.prop(props, "exportpath")

        layout.label(text="------------- Vertex selection sets -------------")
        layout.prop(props, "filename")
        layout.operator("bgs_starfield.havok_extract_uv_indices", icon='EXPORT')
        layout.separator()
        layout.label(text="Manage saved vertex selection files:")
        layout.prop(props, "selectionset_file")
        layout.operator("bgs_starfield.havok_select_vertices_from_file", icon='RESTRICT_SELECT_OFF')
        layout.operator("bgs_starfield.havok_open_uv_folder", icon='FILE_FOLDER')
        layout.separator()
        layout.label(text="------------- Vertex float data -------------")
        layout.prop(props, "export_type", text="Weight Type")
        layout.prop(props, "vertex_group_name")
        layout.operator("bgs_starfield.havok_export_vertex_group_weights", icon='EXPORT')


        layout.separator()
        layout.label(text="------------- Export .hkt/.hkx section -------------")
        layout.prop(props, "fbx_importer_path")
        layout.prop(props, "geometry_bridge_dll_path")
        layout.prop(props, "havok_filtermanager_path")
        layout.prop(props, "havok_filtermanager_settings_path")
        col = layout.column()
        row = col.split(factor=0.8)
        row.operator("bgs_starfield.havok_export_and_run_fbximporter", icon='EXPORT')
        row.prop(props, "run_filtermanager")
        layout.separator()
        layout.label(text="---------- Post process .hkx for starfield ----------")
        layout.prop(props, "havok_cloth_hkx")
        layout.operator("bgs_starfield.havok_cloth_postprocess", icon='EXPORT')