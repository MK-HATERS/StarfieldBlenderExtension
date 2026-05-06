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
import mathutils
import math

from ..utils import bs_plugin_data


class VIEW3D_PT_bgs_starfield_general(bpy.types.Panel):
    bl_idname = bs_plugin_data.bl_id_with_project_suffix(
        "VIEW3D_PT_bgs_starfield_general")
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_label = "General"
    bl_category = "BGS Starfield"
    bl_order = 0

    def draw(self, context):
        layout = self.layout
        layout.separator()

        # Config section
        box = layout.box()
        box.label(text="Config")
        box.prop(context.scene, "assets_folder", text="Asset Folder")
        
        # Import Skeleton Button
        box.operator("object.import_skeleton_from_assets", text="Add Skeleton from Assets", icon='ARMATURE_DATA')

        # Units section
        box = layout.box()
        box.label(text="Units: %s Scale: %.2f" % (
            context.scene.unit_settings.length_unit, context.scene.unit_settings.scale_length))
        from ..operators.export_ops import BGS_STARFIELD_OT_set_recommended_unit_scale
        if context.scene.unit_settings.system != BGS_STARFIELD_OT_set_recommended_unit_scale.RECOMMENDED_UNIT_SYSTEM or context.scene.unit_settings.length_unit != BGS_STARFIELD_OT_set_recommended_unit_scale.RECOMMENDED_LENGTH_UNIT or abs(context.scene.unit_settings.scale_length - BGS_STARFIELD_OT_set_recommended_unit_scale.RECOMMENDED_SCALE_LENGTH) > 0.001:
            box.operator(bs_plugin_data.bl_id_with_project_suffix(
                "bgs_starfield.set_recommended_unit_scale"), icon="ERROR")

        obj = context.active_object
        if obj is None:
            layout.label(text="No active object selected")
            layout.label(text="Select an object to see properties")
            return

        # Basic object info
        box = layout.box()
        box.label(text="Active Object: %s" % (obj.name))
        box.label(text="Type: %s" % (obj.type))

        # Vertex count if mesh
        if obj.type == 'MESH':
            mesh = obj.data
            box.label(text="Vertices: %d" % len(mesh.vertices))
            box.label(text="Edges: %d" % len(mesh.edges))
            box.label(text="Faces: %d" % len(mesh.polygons))

        # Object specific properties
        obj_matrix_local = obj.matrix_local
        box.label(text="T <%.2f, %.2f, %.2f>" % (obj_matrix_local.translation.x,
                  obj_matrix_local.translation.y, obj_matrix_local.translation.z))
        obj_matrix_local_euler = obj_matrix_local.to_euler()
        box.label(
            text="R <%.1f, %.1f, %.1f>" %
            (math.degrees(obj_matrix_local_euler.x),
             math.degrees(obj_matrix_local_euler.y),
             math.degrees(obj_matrix_local_euler.z)))
        obj_matrix_local_scale = obj_matrix_local.to_scale()
        box.label(text="S <%.2f, %.2f, %.2f>" % (
            obj_matrix_local_scale.x, obj_matrix_local_scale.y, obj_matrix_local_scale.z))

        vertex_group_partitions = bs_plugin_data.object_get_bgs_vertex_group_partitions(obj)
        if vertex_group_partitions:
            num_partitions = len(vertex_group_partitions.partitions)
            if num_partitions > 0:
                box.label(text="Partitions: %d Vertex Group(s)" %
                          (num_partitions))

        bgs_object_data = bs_plugin_data.object_get_bgs_object_data(obj)
        if bgs_object_data:
            box = layout.box()
            box.prop(bgs_object_data, "sgo_keep", text="Keep Object", icon='PINNED', emboss=True)
            if bgs_object_data.sgo_keep:
                box.prop(bgs_object_data, "sgo_keep_type",
                         text="Keep Type", emboss=True)

            box.prop(bgs_object_data, "has_parent_attachment",
                     text="Connection Point",
                     icon='CONSTRAINT_BONE', emboss=True)
            if bgs_object_data.has_parent_attachment:
                box_pre = box
                box = box.box()
                box.prop(bgs_object_data,
                         "parent_attachment_name", text="Type",
                         emboss=True)
                if bgs_object_data.parent_attachment_name == "CUSTOM":
                    box.prop(bgs_object_data,
                             "custom_parent_attachment", text="Custom Name",
                             emboss=True)
                box = box_pre

        if obj.type == "ARMATURE":
            try:
                arm = obj.data
                bone = arm.bones.active
                if bone:
                    bone = arm.bones.active
                    bone_par = bone.parent
                    pose_bone = obj.pose.bones[bone.name]
                    pose_bone_par = None
                    if bone_par:
                        pose_bone_par = obj.pose.bones[bone_par.name]
                    par_mat_inv = pose_bone_par.matrix.inverted_safe(
                    ) if pose_bone_par else mathutils.Matrix()
                    bone_matrix_local = par_mat_inv @ pose_bone.matrix

                    box = layout.box()
                    box.label(text="Bone: %s" % (bone.name))
                    box.label(
                        text="T <%.2f, %.2f, %.2f>" %
                        (bone_matrix_local.translation.x, bone_matrix_local.translation.y,
                         bone_matrix_local.translation.z))
                    bone_matrix_local_euler = bone_matrix_local.to_euler()
                    box.label(
                        text="R <%.1f, %.1f, %.1f>" %
                        (math.degrees(bone_matrix_local_euler.x),
                         math.degrees(bone_matrix_local_euler.y),
                         math.degrees(bone_matrix_local_euler.z)))
                    bone_matrix_local_scale = bone_matrix_local.to_scale()
                    box.label(
                        text="S <%.2f, %.2f, %.2f>" %
                        (bone_matrix_local_scale.x, bone_matrix_local_scale.y,
                         bone_matrix_local_scale.z))

                    bone_has_sgo_keep = False
                    armature_bgs_props = bs_plugin_data.armature_get_bgs_props(
                        arm)
                    if armature_bgs_props and hasattr(armature_bgs_props, 'armature_bone_properties'):
                        for armature_bone_property in armature_bgs_props.armature_bone_properties:
                            if armature_bone_property.name == bone.name:
                                bone_has_sgo_keep = armature_bone_property.sgo_keep
                                break
                    box.label(text="Keep Bone: %s" % (bone_has_sgo_keep))
                    box.context_pointer_set("arm", arm)
                    box.context_pointer_set("bone", bone)
                    box.operator(bs_plugin_data.bl_id_with_project_suffix(
                        "bgs_starfield.toggle_armature_bone_sgo_keep"),
                        text="Toggle Keep Bone", icon='HIDE_OFF')

            except BaseException as e:
                print("node_panel armature error: %s" % (e))
                pass


classes = [VIEW3D_PT_bgs_starfield_general]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)