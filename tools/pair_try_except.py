lines=open('scripts/starfield_blender_extension/operators/material_ops.py','r',encoding='utf-8').read().splitlines()
try_lines=[]
except_lines=[]
for i,l in enumerate(lines):
    s=l.strip()
    if s.startswith('try:'):
        try_lines.append(i+1)
    if s.startswith('except ') or s=='except:' or s.startswith('finally:'):
        except_lines.append(i+1)
# pair tries with next except/finally
pairs=[]
used_except=set()
for t in try_lines:
    match=None
    for e in except_lines:
        if e>t and e not in used_except:
            match=e
            used_except.add(e)
            break
    pairs.append((t,match))
for p in pairs:
    print(p)
unmatched=[t for t,m in pairs if m is None]
print('unmatched tries:', unmatched)
print('counts', len(try_lines), len(except_lines))
