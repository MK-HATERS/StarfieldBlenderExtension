import sys, py_compile, traceback
p = sys.argv[1]
try:
    py_compile.compile(p, doraise=True)
    print('COMPILE_OK')
except Exception:
    traceback.print_exc()
    sys.exit(1)
