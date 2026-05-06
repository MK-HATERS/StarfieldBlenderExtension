p='scripts/starfield_blender_extension/operators/material_ops.py'
with open(p,'rb') as f:
    data = f.read()
print('len', len(data))
lines = data.split(b'\n')
for i,l in enumerate(lines[:400]):
    print(f'{i+1:04d}:', repr(l))
