lines=open('scripts/starfield_blender_extension/operators/material_ops.py','r',encoding='utf-8').read().splitlines()
try_lines=[142,148,155,176,225,310,314,323,334,341,349,355,361]
for ln in try_lines:
    print('----',ln,'----')
    for i in range(ln-3, ln+6):
        if 0<=i<len(lines):
            print(f"{i+1:04d}: {lines[i]}")
    print()
