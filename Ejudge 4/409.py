import sys

n = int(input())

def powers_of_two(limit):
    value = 1
    for _ in range(limit + 1):
        yield value
        value *= 2

first = True
for p in powers_of_two(n):
    if not first:
        sys.stdout.write(" ")
    sys.stdout.write(str(p))
    first = False