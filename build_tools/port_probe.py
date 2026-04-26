import random
import socket

ok = 0
fail = 0
errs = {}

for _ in range(500):
    p = random.randint(49152, 65535)
    s = socket.socket()
    try:
        s.bind(("127.0.0.1", p))
        ok += 1
    except OSError as e:
        fail += 1
        code = getattr(e, "winerror", None)
        errs[code] = errs.get(code, 0) + 1
    finally:
        s.close()

print("ok", ok, "fail", fail, "errs", errs)
