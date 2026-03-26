import sys

data = sys.stdin.read().splitlines()
m = int(data[0])

g = 0 

def outer():
    n = 0  

    def inner(cmd, value):
        nonlocal n
        global g

        if cmd == "global":
            g += value
        elif cmd == "nonlocal":
            n += value
        elif cmd == "local":
            x = 0
            x += value  

    for i in range(1, m + 1):
        scope, val = data[i].split()
        inner(scope, int(val))

    return n

final_n = outer()

print(g, final_n)