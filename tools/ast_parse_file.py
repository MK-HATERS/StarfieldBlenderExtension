import ast, sys
p = sys.argv[1]
try:
    s = open(p, 'r', encoding='utf-8').read()
    ast.parse(s)
    print('OK')
except Exception as e:
    print(type(e).__name__ + ':', e)
    import traceback; traceback.print_exc()
