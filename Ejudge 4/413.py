import sys
import json

def tokenize(path: str):
    # returns list of tokens: ('key', str) or ('idx', int)
    tokens = []
    i = 0
    n = len(path)
    while i < n:
        if path[i] == '.':
            i += 1
            continue
        if path[i] == '[':
            j = path.find(']', i)
            if j == -1:
                return None
            idx_str = path[i+1:j]
            if not idx_str.isdigit():
                return None
            tokens.append(('idx', int(idx_str)))
            i = j + 1
        else:
            j = i
            while j < n and path[j] not in '.[':
                j += 1
            key = path[i:j]
            if key == "":
                return None
            tokens.append(('key', key))
            i = j
    return tokens

def resolve(obj, tokens):
    cur = obj
    for typ, val in tokens:
        if typ == 'key':
            if isinstance(cur, dict) and val in cur:
                cur = cur[val]
            else:
                return None, False
        else:  # idx
            if isinstance(cur, list) and 0 <= val < len(cur):
                cur = cur[val]
            else:
                return None, False
    return cur, True

lines = sys.stdin.read().splitlines()
J = json.loads(lines[0].strip())
q = int(lines[1].strip())

out = []
for k in range(q):
    query = lines[2 + k].strip()
    tokens = tokenize(query)
    if tokens is None:
        out.append("NOT_FOUND")
        continue
    value, ok = resolve(J, tokens)
    if not ok:
        out.append("NOT_FOUND")
    else:
        out.append(json.dumps(value, separators=(",", ":"), ensure_ascii=False))

sys.stdout.write("\n".join(out))