p='scripts/starfield_blender_extension/operators/material_ops.py'
with open(p,'r',encoding='utf-8') as f:
    lines=f.readlines()
ln=373
print('Total lines:', len(lines))
for i in range(360,380):
    print(f'{i+1}:', repr(lines[i]))
