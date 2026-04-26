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

import importlib
import inspect
import os
import re
import sys

import bpy


ROOT_PATH = os.path.dirname(__file__).replace(
    os.sep + "utils", "").replace(os.sep + "app_utils", "")

# NOTE: if a class isn't registering when you think it should be (has the correct class code embedded in it), make sure it has a bl_idname attribute!!
# Operator, Menu, Panel, UI List, Property Group#
class_codes = ["OT", "MT", "PT", "UL", "PG", "TOOL"]


class AppUtils():

    @staticmethod
    def get_guid():
        import uuid
        return uuid.uuid4().hex

    @staticmethod
    def purge_orphans():
        # adapted from a PowerSave utility function of the same name

        # TODO: collect the number of items per type we removed and print it out

        collections = []

        for attr in dir(bpy.data):
            item = getattr(bpy.data, attr, None)
            if isinstance(item, bpy.types.bpy_prop_collection):
                collections.append(item)

        purged = 0

        # purge any objects that are not in a collection (the user has no way of knowing they even exist!)
        # do this first because removing the objects could create orphaned data we'll catch in the recursive loop
        for o in bpy.data.objects:
            if not o.users_collection:
                bpy.data.objects.remove(o)
                purged += 1

        while True:
            before = sum(len(x) for x in collections)

            for collection in collections:
                for item in collection:
                    if item.users == 0:
                        collection.remove(item)

            after = sum(len(x) for x in collections)

            if before > after:
                purged += before - after
            else:
                break

        # ViewportInterface.print(f'Deleted <fg=cyan>{purged} <fg=white>data-block(s)', duration=15)
        return purged

    @staticmethod
    def unregister_tool(idname, space_type, context_mode):
        from bl_ui.space_toolsystem_common import ToolSelectPanelHelper
        cls = ToolSelectPanelHelper._tool_class_from_space_type(space_type)
        tools = cls._tools[context_mode]

        for i, tool_group in enumerate(tools):
            if isinstance(tool_group, tuple):
                for t in tool_group:
                    if 'ToolDef' in str(type(t)) and t.idname == idname:
                        if len(tools[i]) == 1:
                            # it's a group with a single item, just remove it from the tools list.
                            tools.pop(i)
                        else:
                            tools[i] = tuple(
                                x for x in tool_group if x.idname != idname)
                        break
            elif tool_group is not None:
                if tool_group.idname == idname:
                    tools.pop(i)
                    break

        # cleanup any doubled up separators left over after removing a tool
        for i, p in enumerate(reversed(tools)):
            if i < len(tools)-2 and tools[i] is None and tools[i+1] is None:
                tools.pop(i)

    @staticmethod
    def is_addon_enabled(addon_name):
        '''Given an addon_name, returns the enabled status of that addon (or None if the addon wasn't found). Useful for cross-addon functionality'''
        from addon_utils import check, paths
        for category in [bpy.path.module_names(p) for p in paths()]:
            for name, path in category:
                if name == addon_name:
                    return check(name)[1]
        return None  # addon not found

    @staticmethod
    def enable_addon(addon_name):
        '''Given an addon_name, enables it (if it exists) and returns a tuple: was_enabled, is_enabled'''
        addon_enabled = AppUtils.is_addon_enabled(addon_name)
        if addon_enabled is None:
            print(f'Tried to enable an addon that was not found: {addon_name}')
            return (False, False)
        if not addon_enabled:
            try:
                bpy.ops.preferences.addon_enable(module=addon_name)
            except AttributeError:
                pass
            import addon_utils
            addon_utils.enable(addon_name, persistent=True)
            print(f'{addon_name} was not enabled, but now it is.')
            return (False, AppUtils.is_addon_enabled(addon_name))
        return (True, True)

    @staticmethod
    def disable_addon(addon_name):
        '''Given an addon_name, disables it (if it exists) and returns a tuple: was_enabled, is_enabled'''
        addon_enabled = AppUtils.is_addon_enabled(addon_name)
        if addon_enabled is None:
            print(f'Tried to enable an addon that was not found: {addon_name}')
            return (False, False)
        if addon_enabled:
            try:
                bpy.ops.preferences.addon_disable(module=addon_name)
            except AttributeError:
                pass
            import addon_utils
            addon_utils.disable(addon_name)
            print(f'{addon_name} was enabled, but now it is not.')
            return (True, AppUtils.is_addon_enabled(addon_name))
        return (False, False)

    @staticmethod
    def get_module_function(module_fullname, func_name):
        module = AppUtils.get_loaded_module_by_name(module_fullname)
        funcs = {}
        try:
            for name, func in inspect.getmembers(module, inspect.isfunction):
                funcs[name] = func
            if func_name in funcs:
                return funcs[func_name]
        except ReferenceError:
            pass
        return None

    @staticmethod
    def get_module_classes(module_fullname):
        module = AppUtils.get_loaded_module_by_name(module_fullname)
        members = {}
        try:
            for name, obj in inspect.getmembers(module, inspect.isclass):
                members[name] = obj
        except ReferenceError:
            pass
        return members

    @staticmethod
    def get_class_by_name(module_object, class_name):
        for name, obj in inspect.getmembers(module_object, inspect.isclass):
            if name == class_name:
                return obj
        return None

    @staticmethod
    def get_loaded_module_by_name(fullname):
        assert fullname in sys.modules, f"Could not find a loaded module with the name '{fullname}'"
        return sys.modules[fullname]

    @staticmethod
    def import_modules(import_paths, debug_output=False):
        '''
        Given a list of folders relative to the root of the project, load all of the modules within those folders (in the order they are listed).
        Modules themselves are loaded alphabetically. Excludes subdirectories, or modules that begin with "!"
        '''
        assert isinstance(
            import_paths, list), "Expected a list of folders to search for modules, got something else."

        from ... import registered_callbacks
        from ... import registered_classes

        registered_callbacks = []
        registered_classes = []

        # throw any of the addon-related modules that are currently loaded into a list.
        already_imported = sorted(
            [key for key in sys.modules if key.startswith(AppUtils.get_addon_name())])

        # a list of modules that we should NOT import if found during a scan.
        exclude = []  # ['debug', 'prefs', 'meta', 'definitions', 'init']

        for p in import_paths:
            if debug_output:
                print(
                    f"Importing modules from path '{AppUtils.get_addon_name() + os.sep + p + os.sep}':")
            for module in sorted([f.name.replace(".py", "")
                                  for f in os.scandir(ROOT_PATH + os.sep + p)
                                  if not f.name.startswith("!") and f.name.endswith('.py') and
                                  not f.is_dir()]):
                if module in exclude or module == '__init__':
                    continue
                try:
                    module_full_name = f"{AppUtils.get_addon_name()}.{p}.{module}"
                    if debug_output:
                        print(
                            f"  importing {AppUtils.get_addon_name()}.{p}.{module}")
                    # Prevent double loading by checking sys.modules to see if this module is already in memory. if so, use importlib- otherwise import normally.
                    if module_full_name not in already_imported:
                        exec(f"from ... {p} import {module}")
                    else:
                        importlib.reload(sys.modules[module_full_name])
                    AppUtils.register_module_classes(
                        sys.modules[module_full_name], debug_output)
                except BaseException as e:
                    print("AppUtils:import_modules exception for path(%s) module(%s) (%s)" % (
                        p, module, e))

        if debug_output:
            print(
                f"Finished registering {len(registered_classes)} classes and {len(registered_callbacks)} custom callbacks")

    @staticmethod
    def get_addon_prefs(context=None):
        if context is None:
            context = bpy.context
        return context.preferences.addons[AppUtils.get_addon_name()].preferences

    @staticmethod
    def register_module_classes(module, debug_output=False):
        register_objects = {}

        from ... import registered_callbacks
        from ... import registered_classes

        patterns = [re.compile(r'[A-Z][A-Z0-9_]*_'+c+'_[A-Za-z0-9_]+')
                    for c in class_codes]

        # to make sure classes are registered in a top-down fashion rather than alphabetically, we have to use the module's ordered dictionary and create a sorted list
        ordered_modules = [(m, getattr(module, m)) for m in module.__dict__.keys(
        ) if inspect.isclass(getattr(module, m))]
        for name, obj in ordered_modules:
            for pattern in patterns:
                if pattern.search(name) and name not in registered_classes:
                    registered_classes.append(obj)
                    register_objects[name] = obj
                    break
            else:
                if '.tools.' in obj.__module__:
                    registered_classes.append(obj)
                    register_objects[name] = obj

        for name, func in inspect.getmembers(module, lambda o: inspect.isfunction(o)):
            if name in {'register_custom'}:
                func()
            elif name in {'unregister_custom'}:
                registered_callbacks.append(func)

        for name, reg_class in register_objects.items():
            try:
                # only tools have the bgs_starfield_tool_info attribute
                if hasattr(reg_class, "bgs_starfield_tool_info"):
                    bpy.utils.register_tool(
                        reg_class,
                        after=reg_class.bgs_starfield_tool_info.get(
                            "after", None),
                        separator=reg_class.bgs_starfield_tool_info.get(
                            "separator", False),
                        group=reg_class.bgs_starfield_tool_info.get(
                            "group", False)
                    )
                else:
                    if debug_output:
                        print(f"    Registering class: {name}")
                    bpy.utils.register_class(reg_class)
            except ValueError:
                # already registered, skip it
                pass
            except BaseException as e:
                if '_TOOL_' in name:
                    print(f"Could not register {name}: {e}")
                    pass
                else:
                    raise

        for name, func in inspect.getmembers(module, lambda o: inspect.isfunction(o)):
            if name in {'late_register'}:
                func()

    @staticmethod
    def unload_modules(debug_output=False):
        from ... import registered_callbacks
        from ... import registered_classes

        if debug_output:
            print(
                f"Unloading modules... {len(registered_classes)} classes, {len(registered_callbacks)} custom callbacks")
        for callback in registered_callbacks:
            try:
                callback()
            except BaseException as e:
                print("AppUtils:unload_modules callback error(%s)" % (e))
        for c in registered_classes:
            if debug_output:
                print(f"    Unregistering class: {c.__name__}")
            try:
                if hasattr(c, "bgs_starfield_tool_info"):
                    bpy.utils.unregister_tool(c)
                else:
                    bpy.utils.unregister_class(c)
            except RuntimeError:
                pass
            except AttributeError as e:
                if "_TOOL_" in c.__name__:
                    print(f"Could not unregister {c.__name__}: {e}")

    @staticmethod
    def find_registered_operator(rna_name):
        # print(f"Trying to find '{rna_name}' in bpy.types..")
        obj = getattr(bpy.types, rna_name, False)

        if obj:
            return obj

        # print("Couldnt find it!")
        return None

    @staticmethod
    def get_addon_name():
        return __name__.partition('.')[0]

    @staticmethod
    def get_preferences():
        if AppUtils.get_addon_name() in bpy.context.preferences.addons:
            return bpy.context.preferences.addons[AppUtils.get_addon_name()].preferences
        return None

    @staticmethod
    def get_pref_value(key):
        if not hasattr(AppUtils.get_preferences(), key):
            # TODO: need to figure out a way to ignore this issue if Blender has just started, because it will always happen when using the vscode extension
            # print(f"Could not find a preference named '{key}' in the preferences class.")
            return None
        return getattr(AppUtils.get_preferences(), key)

    @staticmethod
    def get_modules_by_path(path):
        path = path.replace("/", os.sep)
        path = path.replace("\\", os.sep)
        if not path.startswith(os.sep):
            path = os.sep + path
        module_parent = path.replace(os.sep, ".")

        modules = []
        for m in [
                f.name.replace(".py", "") for f in os.scandir(ROOT_PATH + path)
                if not f.is_dir() and not f.name.startswith("!")]:
            module = sys.modules.get(
                f"{ AppUtils.get_addon_name() }{ module_parent }.{ m }")
            if module:
                modules.append(module)
        return modules

    @staticmethod
    def event_modifiers_match(event_a, event_b):
        '''Compares two events to see if the modifiers are the same. Handles the odd 'any' case so you don't have to worry about it.'''
        if event_a.any or event_b.any:
            return True

        return (event_a.shift == event_b.shift and
                event_a.ctrl == event_b.ctrl and
                event_a.alt == event_b.alt)

    @staticmethod
    def get_full_keybind_string(kmi, props=True):
        import idprop

        output = f"{kmi.type} [{kmi.value}]"
        if kmi.any:
            output = "ANY+" + output
        else:
            if kmi.shift:
                output = "SHIFT+" + output
            if kmi.alt:
                output = "ALT+" + output
            if kmi.ctrl:
                output = "CTRL+" + output
        propstring = ""
        if props and hasattr(kmi, "properties") and kmi.properties is not None:
            for key in kmi.properties.keys():
                if isinstance(kmi.properties[key], idprop.types.IDPropertyGroup):
                    propstring += f"{key}: {kmi.properties[key]}, "
                else:
                    propstring += f"MACRO: {key}, "

        return f"{kmi.idname}: {output} {propstring}"

    @staticmethod
    def find_areas_by_type(area_type):
        # this workspace has no screens, or we're in the middle of a reload, or we're in CLI mode.
        if not bpy.context.workspace or not bpy.context.workspace.screens:
            return []
        return [a for a in bpy.context.workspace.screens[0].areas if a.type == area_type]

    @staticmethod
    def get_region_coords_by_ratio(r, x=.5, y=.5):
        '''Givent a region "r", return the 2D screen coordinates for a given ratio. For example, if x and y are both .5, the exact center of the region will be returned.'''

        cx = r.x + ((r.width - r.x) * x)
        cy = r.y + ((r.height - r.y) * y)

        return (int(cx), int(cy))

    @staticmethod
    def get_context_override(area_type='VIEW_3D'):
        ''' Iterates through the blender GUI's windows, screens, areas, regions to find the View3D space and its associated window.  Populate an 'oContextOverride context' that can be used with bpy.ops that require to be used from within a View3D (like most addon code that runs of View3D panels) '''
        # SOURCE: https://www.blender.org/forum/viewtopic.php?t=27834
        # NOTE: If your operator fails the log will show an "PyContext: 'xyz' not found".  To fix stuff 'xyz' into the override context and try again!
        override = bpy.context.copy()
        # TODO: Find way to avoid doing four levels of traversals at every request!!
        for window in bpy.context.window_manager.windows:
            screen = window.screen
            for area in screen.areas:
                if area.type == area_type:                         # Frequently, bpy.ops operators are called from View3d's toolbox or property panel.  By finding that window/screen/area we can fool operators in thinking they were called from the View3D!
                    for region in area.regions:
                        # View3D has several 'windows' like 'HEADER' and 'WINDOW'.  Most bpy.ops require 'WINDOW'
                        if region.type == 'WINDOW':
                            override.update({
                                'window': window,
                                'screen': screen,
                                'area': area,
                                'region': region,
                                'scene': bpy.context.scene,
                            })
                            # print("-AssembleOverrideContextForView3dOps() created override context: ", oContextOverride)
                            return override
        return None
        # raise Exception("ERROR: AssembleOverrideContextForView3dOps() could not find a VIEW_3D with WINDOW region to create override context to enable View3D operators.  Operator cannot function.")

    @staticmethod
    def remove_sidebar_panel(panel_class_name):
        '''Given a panel class name (str), remove the panel from the N-panel (sidebar)'''
        if hasattr(bpy.types, panel_class_name):
            panel = getattr(bpy.types, panel_class_name)
            # print(f"Removing sidebar panel class {panel_class_name}")
            # TODO: find any panels that have a bl_parent_id that matches panel_class_name and remove those as well
            try:
                # change the region to 'WINDOW' to avoid the panel being dumped back into the 'Misc' tab
                panel.bl_region_type = 'WINDOW'
                del panel.bl_category
            except AttributeError:
                # print(f"{panel_class_name} was already removed")
                pass
            bpy.utils.unregister_class(panel)
            bpy.utils.register_class(panel)
        # else:
            # print(f"Couldn't find {panel_class_name}")

    @staticmethod
    def get_panel_by_category(category):
        '''Given a panel class name (str), remove the panel from the N-panel (sidebar)'''
        return [p for p in bpy.types.Panel.__subclasses__() if hasattr(p, 'bl_category') and p.bl_category == category]

    @staticmethod
    def set_panel_category(panel, category):
        if not isinstance(panel, list):
            panel = [panel]

        for p in panel:
            try:
                p.bl_category = category
                bpy.utils.unregister_class(p)
                bpy.utils.register_class(p)
            except AttributeError:
                pass

    @staticmethod
    def report_warning(op, msg, verbose_msg=None):
        '''For the "op" parameter, pass in "self" if calling from an operator class'''
        op.report({'WARNING'}, msg)
        if verbose_msg:
            # TODO: this should go to the viewport interface
            print(str(verbose_msg))
        return {'CANCELLED'}

    @staticmethod
    def report_error(op, msg, verbose_msg=None):
        '''For the "op" parameter, pass in "self" if calling from an operator class'''
        if verbose_msg:
            # TODO: this should go to the viewport interface
            print(str(verbose_msg))
        # this will raise an exception so it needs to be done after we print our verbose message
        op.report({'ERROR'}, msg)
        return {'CANCELLED'}

    @staticmethod
    def report(op, msg, verbose_msg=None):
        '''For the "op" parameter, pass in "self" if calling from an operator class'''
        op.report({'INFO'}, msg)
        if verbose_msg:
            # TODO: this should go to the viewport interface
            print(str(verbose_msg))
        return {'FINISHED'}
