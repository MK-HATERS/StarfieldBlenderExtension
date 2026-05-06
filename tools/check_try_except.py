p='scripts/starfield_blender_extension/operators/material_ops.py'
lines=open(p,'r',encoding='utf-8').read().splitlines()
try_lines=[]
except_lines=[]
for i,l in enumerate(lines):
    s=l.strip()
    if s.startswith('try:'):
        try_lines.append(i+1)
    if s.startswith('except ' ) or s=='except:' or s.startswith('finally:'):
        except_lines.append(i+1)
print('try count', len(try_lines), 'except/finally count', len(except_lines))
print('tries:', try_lines[:20])
print('excepts/finally:', except_lines[:20])
# show imbalance before line 373
try_before=[ln for ln in try_lines if ln<373]
except_before=[ln for ln in except_lines if ln<373]
print('before 373: try', len(try_before), 'except/finally', len(except_before))
print('try lines before 373:', try_before)
print('except/finally before 373:', except_before)
