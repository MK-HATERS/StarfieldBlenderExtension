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
import typing
import math
import os
from bpy_extras.io_utils import ImportHelper
from ..utils import bs_plugin_data

from ..utils import get_starfield_data_path_with_trailing_slash, show_message_box
from ..utils import utils_blender


class BGS_STARFIELD_OT_load_path_material(bpy.types.Operator):
    bl_label = "Load textures to blender material"
    bl_idname = bs_plugin_data.bl_id_with_project_suffix(
        "bgs_starfield.load_path_material")
    bl_description = "Load loose textures from Starfield Data folder (defined in Addon preferences) to Blender Material."
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        target_mat = context.active_object.active_material
        if target_mat is None:
            return {'CANCELLED'}
        if not target_mat.use_nodes:
            show_message_box("(Failed) material does not use nodes")
            return {'CANCELLED'}

        starfield_data_path = get_starfield_data_path_with_trailing_slash()

        if not os.path.isdir(starfield_data_path):
            show_message_box(
                "Addon preferences-defined starfield data directory does not exist(%s)" %
                (starfield_data_path))
            return {'CANCELLED'}

        diffuse_path = starfield_data_path + \
            bs_plugin_data.material_get_bgs_props(target_mat).texture_diffuse
        normal_path = starfield_data_path + \
            bs_plugin_data.material_get_bgs_props(target_mat).texture_normal

        if not os.path.isfile(diffuse_path):
            show_message_box(
                "Diffuse texture not found (%s)" % (diffuse_path))
            return {'CANCELLED'}

        if not os.path.isfile(normal_path):
            show_message_box(
                "Diffuse texture not found (%s)" % (normal_path))
            return {'CANCELLED'}

        target_mat.node_tree.links.clear()
        target_mat.node_tree.nodes.clear()

        tex_diffuse = target_mat.node_tree.nodes.new(type='ShaderNodeTexImage')
        tex_normal = target_mat.node_tree.nodes.new(type='ShaderNodeTexImage')
        node_shader = target_mat.node_tree.nodes.new(
            type='ShaderNodeBsdfPrincipled')
        output = target_mat.node_tree.nodes.new(
            type='ShaderNodeOutputMaterial')

        tex_diffuse.image = bpy.data.images.load(diffuse_path)
        tex_normal.image = bpy.data.images.load(normal_path)

        target_mat.node_tree.links.new(tex_diffuse.outputs.get(
            "Color"), node_shader.inputs.get("Base Color"))
        target_mat.node_tree.links.new(tex_normal.outputs.get(
            "Color"), node_shader.inputs.get("Normal"))
        target_mat.node_tree.links.new(node_shader.outputs.get(
            "BSDF"), output.inputs.get("Surface"))

        return {'FINISHED'}


class BGS_STARFIELD_OT_import_mat(bpy.types.Operator, ImportHelper):
    """Import a Starfield .mat file and populate a Blender material"""
    bl_label = "Import .mat to Blender Material"
    bl_idname = bs_plugin_data.bl_id_with_project_suffix(
        "bgs_starfield.import_mat")
    bl_description = "Import a Starfield .mat file (from the game's Data/materials) into a Blender material"
    bl_options = {'REGISTER', 'UNDO'}

    filename_ext = ".mat"
    filter_glob: bpy.props.StringProperty(default="*.mat", options={'HIDDEN'})
    apply_to_active: bpy.props.BoolProperty(
        name="Apply to Active Material",
        description="If enabled, import data will be applied to the active object's material. Otherwise a new material will be created.",
        default=True
    )
    skip_textures: bpy.props.BoolProperty(
        name="Skip Textures",
        description="If enabled, the importer will not attempt to load texture files.",
        default=False
    )
    skip_alpha: bpy.props.BoolProperty(
        name="Skip Alpha Settings",
        description="If enabled, do not import alpha/test settings from the .mat",
        default=False
    )
    force_two_sided: bpy.props.EnumProperty(
        items=[('AUTO', 'Auto', 'Respect shader model'),
               ('ON', 'Force On', 'Force two-sided'),
               ('OFF', 'Force Off', 'Force single-sided')],
        name='Two-Sided',
        default='AUTO'
    )
    use_texconv: bpy.props.BoolProperty(
        name='Use texconv for DDS',
        description='If enabled and texconv is available, convert DDS files to PNG for Blender to load',
        default=False
    )
    override_shader_model: bpy.props.StringProperty(
        name="Override Shader Model",
        description="Optional shader model filename to override what's in the .mat",
        default=""
    )
    rename_material_on_import: bpy.props.BoolProperty(
        name="Rename Material on Import",
        description="When enabled, importing a .mat will rename the target material to match the .mat filename",
        default=True
    )

    def invoke(self, context, event):
        # default directory -> <starfield data>/materials
        try:
            starfield_data_path = get_starfield_data_path_with_trailing_slash()
            default_dir = os.path.join(starfield_data_path, "materials")
            if os.path.isdir(default_dir):
                # open file selector rooted at materials folder
                # Set both directory and filepath to ensure Blender's file browser opens at the desired folder
                try:
                    self.directory = default_dir
                    # set filepath to a folder path (some Blender versions honor filepath)
                    self.filepath = os.path.join(default_dir, "")
                    # ensure filter is set for .mat files
                    self.filter_glob = "*.mat"
                except Exception:
                    try:
                        setattr(self, 'directory', default_dir)
                    except Exception:
                        self.filepath = default_dir
                context.window_manager.fileselect_add(self)
                return {'RUNNING_MODAL'}
        except Exception:
            pass
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

    def execute(self, context):
        import json
        from .. import MaterialConverter
        from ..utils import utils_material

        filepath = getattr(self, 'filepath', None)
        if not filepath or not os.path.isfile(filepath):
            self.report({'ERROR'}, f"File not found or not a file: {filepath}")
            return {'CANCELLED'}

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except Exception as e:
            self.report({'ERROR'}, f"Failed to parse .mat: {e}")
            return {'CANCELLED'}

        # Find or create material to populate depending on apply_to_active
        active_obj = context.active_object
        # desired material name is the basename of the .mat file
        desired_name = os.path.splitext(os.path.basename(filepath))[0]
        if self.apply_to_active and active_obj is not None and active_obj.active_material is not None:
            mat = active_obj.active_material
        else:
            # create a new shader material using helper
            mat = utils_material.new_mat(desired_name)
            # optionally assign to active object if requested
            if self.apply_to_active and active_obj is not None:
                active_obj.active_material = mat

        # Ensure the material is an SF material
        if not utils_material.is_mat(mat):
            # Convert to SF material
            temp_mat = utils_material.new_mat(mat.name)
            mat.use_nodes = True
            # Copy the SF group node from temp_mat
            for node in temp_mat.node_tree.nodes:
                if node.bl_idname == 'ShaderNodeGroup':
                    group_node = mat.node_tree.nodes.new('ShaderNodeGroup')
                    group_node.node_tree = node.node_tree
                    group_node.location = node.location
                    # Connect to Material Output
                    output_node = mat.node_tree.nodes['Material Output']
                    mat.node_tree.links.new(group_node.outputs[0], output_node.inputs[0])
                    break  # Only one group
            bpy.data.materials.remove(temp_mat)

        # Rename the material to match the imported .mat file name (applies to active or new materials)
        try:
            if self.rename_material_on_import:
                if mat.name != desired_name:
                    mat.name = desired_name
        except Exception:
            pass

        material_bgs_props = bs_plugin_data.material_get_bgs_props(mat)

        # base data path
        starfield_data_path = get_starfield_data_path_with_trailing_slash()

        # parse components for textures and shader/alpha settings
        texture_map = {}
        shader_model = None
        alpha_threshold = None

        objs = data.get('Objects', [])
        # Build id->object map for layered material resolution
        objs_by_id = {}
        for obj in objs:
            obj_id = obj.get('ID', None)
            if obj_id:
                objs_by_id[obj_id] = obj

        # helper to normalize filename
        def _norm_relpath(fn: str):
            if fn is None:
                return None
            # replace forward slashes with backslashes and normalize leading 'Data\\'
            fn_norm = fn.replace('/', '\\')
            rel = fn_norm
            if rel.lower().startswith('data\\'):
                rel = rel[5:]
            return rel

        # First, attempt to resolve layered material -> layer -> material -> textureset chain
        try:
            # find the root layered material object (contains a LayerID component)
            layered_root = None
            for obj in objs:
                for comp in obj.get('Components', []):
                    if comp.get('Type') == 'BSMaterial::LayerID':
                        layered_root = obj
                        break
                if layered_root:
                    break

            texture_set_obj = None
            uv_stream_exists = False

            if layered_root is not None:
                # get LayerID value
                layer_id = None
                for comp in layered_root.get('Components', []):
                    if comp.get('Type') == 'BSMaterial::LayerID':
                        layer_id = comp.get('Data', {}).get('ID')
                        break

                if layer_id and layer_id in objs_by_id:
                    layer_obj = objs_by_id.get(layer_id)
                    # layer -> MaterialID, UVStreamID
                    material_id = None
                    uv_id = None
                    for comp in layer_obj.get('Components', []):
                        if comp.get('Type') == 'BSMaterial::MaterialID':
                            material_id = comp.get('Data', {}).get('ID')
                        if comp.get('Type') == 'BSMaterial::UVStreamID':
                            uv_id = comp.get('Data', {}).get('ID')

                    if uv_id and uv_id in objs_by_id:
                        uv_stream_exists = True

                    if material_id and material_id in objs_by_id:
                        material_obj = objs_by_id.get(material_id)
                        # material_obj should contain a TextureSetID component
                        texture_set_id = None
                        for comp in material_obj.get('Components', []):
                            if comp.get('Type') == 'BSMaterial::TextureSetID':
                                texture_set_id = comp.get('Data', {}).get('ID')
                                break

                        if texture_set_id and texture_set_id in objs_by_id:
                            texture_set_obj = objs_by_id.get(texture_set_id)

            # if we found a texture set object, collect its MRTextureFile entries
            if texture_set_obj is not None:
                for comp in texture_set_obj.get('Components', []):
                    if comp.get('Type') == 'BSMaterial::MRTextureFile':
                        idx = comp.get('Index', None)
                        fn = comp.get('Data', {}).get('FileName', None)
                        rel = _norm_relpath(fn)
                        if idx is not None and rel is not None:
                            texture_map[int(idx)] = rel

            # mark UV settings visibility if uv stream exists
            if uv_stream_exists:
                material_bgs_props.show_uv_settings = True
        except Exception:
            # fall back to greedy collection if layered resolution fails
            texture_map = {}
            for obj in objs:
                for comp in obj.get('Components', []):
                    if comp.get('Type') == 'BSMaterial::MRTextureFile':
                        idx = comp.get('Index', None)
                        fn = comp.get('Data', {}).get('FileName', None)
                        rel = _norm_relpath(fn)
                        if idx is not None and rel is not None:
                            texture_map[int(idx)] = rel

        # still collect other non-texture components for shader/alpha/etc
        color_component = None
        for obj in objs:
            for comp in obj.get('Components', []):
                t = comp.get('Type', '')
                if t == 'BSMaterial::ShaderModelComponent':
                    shader_model = comp.get('Data', {}).get('FileName')
                elif t == 'BSMaterial::AlphaSettingsComponent':
                    alpha_threshold = comp.get('Data', {}).get('AlphaTestThreshold')
                    blender_info = comp.get('Data', {}).get('Blender', {})
                    vc = None
                    if blender_info:
                        vc = blender_info.get('Data', {}).get('VertexColorChannel')
                    if vc is not None:
                        try:
                            mat_vc = MaterialConverter.BlendVertexColorChannel(vc)
                            utils_material.set_alpha_blend_channel(mat, mat_vc)
                        except Exception:
                            pass
                elif t == 'BSMaterial::Color':
                    val = comp.get('Data', {}).get('Value', {}).get('Data', {})
                    try:
                        r = float(val.get('x', 0.0))
                        g = float(val.get('y', 0.0))
                        b = float(val.get('z', 0.0))
                        a = float(val.get('w', 1.0))
                        color_component = (r, g, b, a)
                    except Exception:
                        color_component = None
                elif t == 'BSMaterial::TextureReplacement':
                    enabled = comp.get('Data', {}).get('Enabled', 'false')
                    if str(enabled).lower() == 'true':
                        material_bgs_props.remappable_textures = True
                elif t == 'BSMaterial::MipBiasSetting':
                    disable = comp.get('Data', {}).get('DisableMipBiasHint', 'false')
                    if str(disable).lower() == 'true':
                        material_bgs_props.show_additional_texture_settings = True
                elif t == 'BSMaterial::LayeredEmissivityComponent':
                    data = comp.get('Data', {})
                    enabled = data.get('Enabled', 'false')
                    material_bgs_props.external_emittance = (str(enabled).lower() == 'true')
                    lum = data.get('LuminousEmittance', None)
                    if lum is not None:
                        try:
                            material_bgs_props.emit_color_scale = float(lum) / 432.0
                        except Exception:
                            pass
                    first_tint = data.get('FirstLayerTint', {})
                    if isinstance(first_tint, dict):
                        tv = first_tint.get('Data', {}).get('Value', {}).get('Data', {})
                        if tv:
                            try:
                                tr = float(tv.get('x', 0.0))
                                tg = float(tv.get('y', 0.0))
                                tb = float(tv.get('z', 0.0))
                                material_bgs_props.emit_color = (tr, tg, tb)
                            except Exception:
                                pass

        # apply textures
        if not self.skip_textures:
            import subprocess, tempfile, shutil
            for idx, relpath in texture_map.items():
                try:
                    tex_enum = MaterialConverter.TextureIndex(idx)
                except Exception:
                    continue

                fullpath = os.path.normpath(os.path.join(starfield_data_path, relpath))
                # map numeric texture indices to BGS property names (fallback to generic)
                index_to_prop = {
                    0: 'texture_diffuse',
                    1: 'texture_normal',
                    2: 'texture_glow',
                    3: 'texture_height',
                    4: 'texture_environment',
                    5: 'texture_environment_mask',
                    6: 'texture_multilayer',
                    7: 'texture_backlight_mask',
                    8: 'texture_noise',
                }
                prop_name = index_to_prop.get(idx, None)
                if prop_name and hasattr(material_bgs_props, prop_name):
                    setattr(material_bgs_props, prop_name, relpath)
                else:
                    # legacy fallback: try to set by enum name (may not persist on PG)
                    try:
                        setattr(material_bgs_props, f"texture_{tex_enum.name.lower()}", relpath)
                    except Exception:
                        pass

                if not os.path.isfile(fullpath):
                    continue

                img = None
                try:
                    img = bpy.data.images.load(fullpath)
                except Exception:
                    img = None

                # if load failed and file is .dds and texconv allowed, try convert
                if img is None and fullpath.lower().endswith('.dds') and self.use_texconv:
                    preferences = utils_blender.get_preferences()
                    texconv_cmd = preferences.texconv_path or 'texconv'
                    tmpdir = None
                    try:
                        tmpdir = tempfile.mkdtemp(prefix='sf_mat_conv_')
                        out_png = os.path.join(tmpdir, os.path.splitext(os.path.basename(fullpath))[0] + '.png')
                        subprocess.run([texconv_cmd, '-o', tmpdir, '-ft', 'PNG', fullpath], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                        if os.path.isfile(out_png):
                            img = bpy.data.images.load(out_png)
                    except Exception:
                        img = None
                    finally:
                        if tmpdir is not None:
                            try:
                                shutil.rmtree(tmpdir)
                            except Exception:
                                pass

                if img is not None:
                    utils_material.set_texture_map(mat, tex_enum, img)

        # allow override of shader model from operator props
        if self.override_shader_model:
            shader_model = self.override_shader_model

        # shader model -> two_sided flag
        if self.force_two_sided == 'ON':
            material_bgs_props.two_sided_enabled = True
        elif self.force_two_sided == 'OFF':
            material_bgs_props.two_sided_enabled = False
        else:
            if shader_model is not None:
                try:
                    material_bgs_props.two_sided_enabled = not (shader_model == MaterialConverter.ShaderModel.ONE_LAYER_STANDARD.value)
                except Exception:
                    material_bgs_props.two_sided_enabled = False

        # alpha
        if (not self.skip_alpha) and alpha_threshold is not None:
            try:
                material_bgs_props.alpha_enabled = True
                # map threshold to alpha_ref if appropriate
                try:
                    material_bgs_props.alpha_ref = int(float(alpha_threshold))
                except Exception:
                    material_bgs_props.alpha_ref = 0
            except Exception:
                pass

        # Apply parsed surface data to the material node group (base color, opacity, emissive)
        try:
            from ..utils import utils_material
            tree = mat.node_tree
            group_node = utils_material.get_node_tree_BSDF(mat)
            if group_node is not None and tree is not None:
                # Helper: remove any link from a named node to the group's input
                def _remove_link_from(node_from, input_name):
                    try:
                        links = [l for l in tree.links if l.from_node == node_from and l.to_node == group_node and l.to_socket.name == input_name]
                        for l in links:
                            tree.links.remove(l)
                    except Exception:
                        pass

                # If a texture node exists but has no image (load failed) or textures are skipped,
                # disconnect it so the group input default will take effect (or we create a constant node).
                tex_names = ['COLOR', 'NORMAL', 'ROUGH', 'METAL', 'EMISSIVE', 'OPACITY', 'AO', 'HEIGHT']
                for tname in tex_names:
                    tex_node = tree.nodes.get(tname)
                    # if textures are skipped, or node missing or node has no image, disconnect link
                    img_missing = True
                    if tex_node is not None:
                        # For image texture nodes, check image property
                        img = getattr(tex_node, 'image', None)
                        if img is not None:
                            img_missing = False

                    if self.skip_textures or tex_node is None or img_missing:
                        # remove the link from the texture node if present
                        if tex_node is not None:
                            _remove_link_from(tex_node, 'Color')
                        # also remove any direct link to the group's input from any node
                        try:
                            links = [l for l in tree.links if l.to_node == group_node and l.to_socket.name == tname]
                            for l in links:
                                tree.links.remove(l)
                        except Exception:
                            pass

                        # create a simple constant node and link it to the group input to ensure visual result
                        try:
                            if tname in ('COLOR', 'EMISSIVE'):
                                const = tree.nodes.new('ShaderNodeRGB')
                                const.name = f"CONST_{tname}"
                                if tname == 'COLOR' and color_component is not None:
                                    r, g, b, a = color_component
                                    const.outputs[0].default_value = (r, g, b, 1.0)
                                elif tname == 'EMISSIVE':
                                    ec = getattr(material_bgs_props, 'emit_color', None)
                                    esc = getattr(material_bgs_props, 'emit_color_scale', 1.0)
                                    if ec is not None and len(ec) >= 3:
                                        const.outputs[0].default_value = (float(ec[0]) * float(esc), float(ec[1]) * float(esc), float(ec[2]) * float(esc), 1.0)
                                    else:
                                        const.outputs[0].default_value = (0.0, 0.0, 0.0, 1.0)
                                else:
                                    const.outputs[0].default_value = (0.8, 0.8, 0.8, 1.0)
                                tree.links.new(const.outputs[0], group_node.inputs[tname])
                            else:
                                # numeric value nodes for ROUGH/METAL/OPACITY/AO
                                val = tree.nodes.new('ShaderNodeValue')
                                val.name = f"CONST_{tname}"
                                if tname == 'OPACITY':
                                    mat_alpha = getattr(material_bgs_props, 'material_alpha', None)
                                    val.outputs[0].default_value = float(mat_alpha) if mat_alpha is not None else 1.0
                                elif tname == 'ROUGH':
                                    # roughness fallback: use 1 - specular_mult if available, else default 0.5
                                    try:
                                        spec_mult = float(getattr(material_bgs_props, 'specular_mult', 1.0))
                                        val.outputs[0].default_value = max(0.0, min(1.0, 1.0 - spec_mult))
                                    except Exception:
                                        val.outputs[0].default_value = 0.5
                                elif tname == 'METAL':
                                    # use has_custom_specular_color as hint; default 0
                                    val.outputs[0].default_value = 0.0
                                else:
                                    val.outputs[0].default_value = 0.0
                                tree.links.new(val.outputs[0], group_node.inputs[tname])
                        except Exception:
                            pass

        except Exception:
            pass

        # Update view layer after modifications
        bpy.context.view_layer.update()

        self.report({'INFO'}, f"Imported .mat to material '{mat.name}'")
        return {'FINISHED'}


class BGS_STARFIELD_OT_import_mat_with_options(bpy.types.Operator):
    """Show import options, then open the .mat file selector with those options applied"""
    bl_label = "Import .mat (Options)"
    bl_idname = bs_plugin_data.bl_id_with_project_suffix(
        "bgs_starfield.import_mat_with_options")
    bl_options = {'REGISTER', 'UNDO'}

    apply_to_active: bpy.props.BoolProperty(
        name="Apply to Active Material",
        default=True
    )
    skip_textures: bpy.props.BoolProperty(
        name="Skip Textures",
        default=False
    )
    skip_alpha: bpy.props.BoolProperty(
        name="Skip Alpha Settings",
        default=False
    )
    force_two_sided: bpy.props.EnumProperty(
        items=[('AUTO', 'Auto', ''), ('ON', 'On', ''), ('OFF', 'Off', '')],
        name='Two-Sided',
        default='AUTO'
    )
    use_texconv: bpy.props.BoolProperty(
        name='Use texconv for DDS',
        default=False
    )
    override_shader_model: bpy.props.StringProperty(
        name="Override Shader Model",
        description="Optional shader model filename to override what's in the .mat",
        default=""
    )
    rename_material_on_import: bpy.props.BoolProperty(
        name="Rename Material on Import",
        description="When enabled, importing a .mat will rename the target material to match the .mat filename",
        default=True
    )

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def draw(self, context):
        layout = self.layout
        layout.prop(self, 'apply_to_active')
        layout.prop(self, 'skip_textures')
        layout.prop(self, 'skip_alpha')
        layout.prop(self, 'force_two_sided')
        layout.prop(self, 'use_texconv')
        layout.prop(self, 'override_shader_model')
        layout.prop(self, 'rename_material_on_import')

    def execute(self, context):
        # invoke the main import operator with these properties and open file selector
        # operator idnames are suffixed via bs_plugin_data.bl_id_with_project_suffix
        main_bl_id = bs_plugin_data.bl_id_with_project_suffix("bgs_starfield.import_mat")
        try:
            module, opname = main_bl_id.split('.')
            opfunc = getattr(getattr(bpy.ops, module), opname)
            opfunc('INVOKE_DEFAULT',
                   apply_to_active=self.apply_to_active,
                   skip_textures=self.skip_textures,
                   skip_alpha=self.skip_alpha,
                   force_two_sided=self.force_two_sided,
                   use_texconv=self.use_texconv,
                   override_shader_model=self.override_shader_model,
                   rename_material_on_import=self.rename_material_on_import)
        except Exception:
            # fallback: try the plain attribute (older convention)
            try:
                bpy.ops.bgs_starfield.import_mat('INVOKE_DEFAULT',
                                                 apply_to_active=self.apply_to_active,
                                                 skip_textures=self.skip_textures,
                                                 skip_alpha=self.skip_alpha,
                                                 force_two_sided=self.force_two_sided,
                                                 use_texconv=self.use_texconv,
                                                 override_shader_model=self.override_shader_model,
                                                 rename_material_on_import=self.rename_material_on_import)
            except Exception as e:
                self.report({'ERROR'}, f"Failed to invoke import operator: {e}")
                return {'CANCELLED'}
        return {'FINISHED'}


def register():
    bpy.utils.register_class(BGS_STARFIELD_OT_load_path_material)
    bpy.utils.register_class(BGS_STARFIELD_OT_import_mat)
    bpy.utils.register_class(BGS_STARFIELD_OT_import_mat_with_options)

def unregister():
    bpy.utils.unregister_class(BGS_STARFIELD_OT_load_path_material)
    bpy.utils.unregister_class(BGS_STARFIELD_OT_import_mat)
    bpy.utils.unregister_class(BGS_STARFIELD_OT_import_mat_with_options)
