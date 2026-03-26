import sys
import importlib

data = sys.stdin.read().splitlines()
q = int(data[0].strip())

out = []
for i in range(1, q + 1):
    module_path, attr = data[i].split()

    try:
        module = importlib.import_module(module_path)
    except Exception:
        out.append("MODULE_NOT_FOUND")
        continue

    if not hasattr(module, attr):
        out.append("ATTRIBUTE_NOT_FOUND")
        continue

    val = getattr(module, attr)
    out.append("CALLABLE" if callable(val) else "VALUE")

sys.stdout.write("\n".join(out))