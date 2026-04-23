---
name: starfield-blender-addon-instructions
description: "Always-on instructions for the Starfield Blender addon project. Use when: working on Blender addon code, UI panels, operators, imports, structure, packaging. Ensures unified single extension, proper UI organization, and follows ReleaseTemplate for distribution."
---

# Starfield Blender Addon Instructions

## Project Overview
This is a single unified Blender addon for Starfield modding. **Do not create or suggest separate extensions** - everything must be integrated into one addon through `scripts/Starfield_Blender_Extension/`.

## Code Structure and Organization
- **Primary Addon Location**: All code belongs in `scripts/Starfield_Blender_Extension/`.
- **Subfolders**:
  - `ui/`: All UI panels, menus, and interface elements.
  - `operators/`: All operator classes for actions.
  - `types/`: Data type definitions and properties.
  - `utils/`: Utility functions and helpers.
- **Main Entry Point**: `__init__.py` registers all components.
- **Avoid Duplication**: Do not create parallel structures like `Starfield_Blender_Extension/` or separate addons.

## Import Rules
- Use **relative imports** only: `from .ui import MyPanel`, `from ..utils import helper`.
- No absolute imports from outside the addon.
- Ensure `__init__.py` files in subfolders for package imports.

## UI Panel Management
- All UI elements in `ui/` folder.
- Panels must be properly categorized (e.g., `CATEGORY = "BGS Starfield"`).
- Use consistent naming: `ExportMaterialPanel`, `BoneRegionsPanel`.
- Register/unregister in `__init__.py`.
- Ensure panels show in correct areas (Properties window, not N-panel).

## Operators and Types
- Operators in `operators/` with clear names like `ExportMeshOperator`.
- Types in `types/` for properties and data structures.
- Register all in `__init__.py`.

## Distribution and Packaging
- Follow `SFGBDocs/ReleaseTemplate/` exactly for packaging.
- Output to `release_packages/` or `release_packages_corrected/`.
- Ensure single ZIP with all components.

## Building and Testing
- The extension is composed of scripts, profiler, include, src, plus relevant root files.
- The `SFGBDocs/ReleaseTemplate/` represents the original compiled addon structure.
- When making changes to individual elements, compile the extension into `temp_check_dist/starfield_blender_extension` for proper testing.
- Copy the reorganized addon from `scripts/Starfield_Blender_Extension/` to `temp_check_dist/starfield_blender_extension/`.
- Include necessary assets, DLLs, and folders from ReleaseTemplate (Assets/, 3rdparty/, MeshConverter.dll, etc.).
- Update VS Code launch.json and tasks.json to point to `temp_check_dist/starfield_blender_extension` for debugging.
- **DLL Compilation**: The MeshConverter.dll must be compiled from C++ source using Visual Studio. Dependencies (Eigen, DirectXMesh, nlohmann/json, miniball) need to be downloaded and paths configured in MeshConverter.vcxproj. OneDrive cloud files may cause copy issues - use local paths for dependencies.

## Validation and Testing
- After changes, run Blender to test addon loading and UI visibility.
- Check console for import errors or registration issues.
- Verify panels appear in correct locations.

## Commit Rules
- Only commit when explicitly instructed by the user.
- Use descriptive messages for changes.

## Common Pitfalls to Avoid
- Do not suggest or create separate extensions/addons.
- Keep UI elements unified and identifiable.
- Follow the ReleaseTemplate for all distributions.

## Examples

### Adding a New UI Panel
```python
# In ui/new_panel.py
import bpy

class NewPanel(bpy.types.Panel):
    bl_label = "New Panel"
    bl_idname = "BGS_PT_new_panel"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "object"
    bl_category = "BGS Starfield"

    def draw(self, context):
        layout = self.layout
        layout.label(text="New Panel Content")

# In __init__.py
from .ui.new_panel import NewPanel

def register():
    bpy.utils.register_class(NewPanel)

def unregister():
    bpy.utils.unregister_class(NewPanel)
```

### Relative Import
```python
# In operators/export_ops.py
from ..utils.blender_utils import get_preferences
```

This ensures a clean, unified addon structure.