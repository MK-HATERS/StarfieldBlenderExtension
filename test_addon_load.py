import bpy
import sys
import os

# Add the addon path
addon_path = r"G:\GithubWork\StarfieldBlenderExtension\temp_check_dist\starfield_blender_extension"
if addon_path not in sys.path:
    sys.path.insert(0, addon_path)

print("Testing addon loading...")

try:
    # Try to import the addon module
    import starfield_blender_extension
    print("✓ Addon module imported successfully")

    # Try to register it
    starfield_blender_extension.register()
    print("✓ Addon registered successfully")

    print("Addon loaded successfully!")

except Exception as e:
    print(f"✗ Error loading addon: {e}")
    import traceback
    traceback.print_exc()