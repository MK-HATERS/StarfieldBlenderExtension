# Starfield Blender Addon — Claude Code Instructions

## Project Overview
This is a **single unified Blender addon** for Starfield modding. **Do not create or suggest separate extensions** — everything must be integrated into one addon through `scripts/Starfield_Blender_Extension/`.

## Code Structure
- **Primary Addon Location**: All code belongs in `scripts/Starfield_Blender_Extension/`
- **Subfolders**:
  - `ui/` — All UI panels, menus, and interface elements
  - `operators/` — All operator classes for actions
  - `types/` — Data type definitions and properties
  - `utils/` — Utility functions and helpers
- **Main Entry Point**: `__init__.py` registers all components
- **No parallel structures**: Never create a duplicate `Starfield_Blender_Extension/` folder or separate addons

## Import Rules
- Use **relative imports only**: `from .ui import MyPanel`, `from ..utils import helper`
- No absolute imports from outside the addon
- Every subfolder must have an `__init__.py` for package imports

## UI Panels
- All UI elements live in `ui/`
- Category must be `"BGS Starfield"`
- Naming convention: `ExportMaterialPanel`, `BoneRegionsPanel`
- Panels belong in the **Properties window**, not the N-panel
- Register/unregister in `__init__.py`

## Operators & Types
- Operators in `operators/` with clear names like `ExportMeshOperator`
- Types in `types/` for properties and data structures
- Register all in `__init__.py`

## Distribution & Packaging
- Follow `SFGBDocs/ReleaseTemplate/` exactly for packaging
- Output to `release_packages/` or `release_packages_corrected/`
- Single ZIP with all components

## Building & Testing
- The extension is composed of scripts, profiler, include, src, plus relevant root files
- `SFGBDocs/ReleaseTemplate/` represents the original compiled addon structure
- For testing individual changes, compile to `temp_check_dist/starfield_blender_extension`
- Copy from `scripts/Starfield_Blender_Extension/` → `temp_check_dist/starfield_blender_extension/`
- Include Assets/, 3rdparty/, MeshConverter.dll, and other ReleaseTemplate assets
- Update `launch.json` and `tasks.json` to point to `temp_check_dist/starfield_blender_extension` for debugging
- **DLL Compilation**: MeshConverter.dll is compiled from C++ using Visual Studio. Dependencies (Eigen, DirectXMesh, nlohmann/json, miniball) must be downloaded and paths set in `MeshConverter.vcxproj`. Use local paths — OneDrive cloud files cause copy failures.

## Validation
- After changes, run Blender to verify addon loads and UI is visible
- Check console for import errors or registration issues
- Confirm panels appear in the correct locations

## Commit Rules
- **Only commit when explicitly instructed by the user**
- Use descriptive commit messages

## Common Pitfalls
- Never suggest or create separate extensions/addons
- Keep all UI elements unified and identifiable under `BGS Starfield`
- Always follow ReleaseTemplate for distributions

## Code Examples

### New UI Panel
```python
# ui/new_panel.py
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

# __init__.py
from .ui.new_panel import NewPanel

def register():
    bpy.utils.register_class(NewPanel)

def unregister():
    bpy.utils.unregister_class(NewPanel)
```

### Relative Import
```python
# operators/export_ops.py
from ..utils.blender_utils import get_preferences
```
