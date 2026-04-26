import sys
import traceback

sys.path.insert(0, r"c:\Users\Anthony\OneDrive\Modding\StarfieldBlenderExtension\temp_check_dist")
print("PYTHONPATH OK")

try:
    import starfield_blender_extension as addon
    print("IMPORT OK")
    addon.register()
    print("REGISTER OK")
except Exception as e:
    print("REGISTER ERROR:", e)
    traceback.print_exc()
