import sys
p = sys.argv[1]
with open(p, 'rb') as f:
    b = f.read(200)
print(b)
for i,ch in enumerate(b):
    if ch>127:
        print('non-ascii at',i,hex(ch))
        break
