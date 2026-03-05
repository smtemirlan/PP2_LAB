import sys

n = int(input())

def divisible_by_3_and_4(limit):
    for i in range(0, limit + 1, 12):
        yield i

first = True
out = sys.stdout

for x in divisible_by_3_and_4(n):
    if not first:
        out.write(" ")
    out.write(str(x))
    first = False