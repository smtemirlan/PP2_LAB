import json
import sys

source = json.loads(sys.stdin.readline().strip())
patch = json.loads(sys.stdin.readline().strip())

def apply_patch(src, p):

    if not isinstance(p, dict):
        return p


    if not isinstance(src, dict):
        src = {}

    for key, pval in p.items():
        if pval is None:

            src.pop(key, None)
        else:
            sval = src.get(key)
            if isinstance(sval, dict) and isinstance(pval, dict):
                src[key] = apply_patch(sval, pval)
            else:
                src[key] = pval
    return src

result = apply_patch(source, patch)

print(json.dumps(result, separators=(",", ":"), sort_keys=True))