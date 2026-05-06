import ast, sys, traceback
p='scripts/starfield_blender_extension/operators/material_ops.py'
try:
    s=open(p,'r',encoding='utf-8').read()
    ast.parse(s)
    print('OK')
except SyntaxError as e:
    print('SyntaxError:', e.msg)
    print('Line:', e.lineno, 'Offset:', e.offset)
    # print context line
    lines = s.splitlines()
    if e.lineno and 1 <= e.lineno <= len(lines):
        print('Context:', lines[e.lineno-1])
    sys.exit(1)
except Exception:
    traceback.print_exc()
    sys.exit(2)
