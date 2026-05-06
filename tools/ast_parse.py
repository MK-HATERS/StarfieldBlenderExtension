import ast, sys
p='scripts/starfield_blender_extension/operators/material_ops.py'
s=open(p,'r',encoding='utf-8').read()
try:
    ast.parse(s)
    print('PARSE OK')
except SyntaxError as e:
    print('SyntaxError', e.msg, e.lineno, e.offset)
    lines=s.splitlines()
    for i in range(max(0,e.lineno-3), min(len(lines), e.lineno+2)):
        print(i+1, lines[i])
    sys.exit(1)
except Exception as e:
    print('Other error', e)
    sys.exit(2)
