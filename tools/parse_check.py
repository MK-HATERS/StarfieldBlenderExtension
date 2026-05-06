import ast
import sys
p='scripts/starfield_blender_extension/operators/material_ops.py'
try:
    s=open(p,'r',encoding='utf-8').read()
    print('---- file preview (first 2000 chars) ----')
    print(repr(s[:2000]))
    ast.parse(s)
    print('OK')
except Exception as e:
    import traceback
    traceback.print_exc()
    sys.exit(1)
