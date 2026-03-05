import sys

elements = input().split()
k = int(input())

def limited_cycle(lst, times):
    for _ in range(times):
        for item in lst:
            yield item

first = True
for value in limited_cycle(elements, k):
    if not first:
        sys.stdout.write(" ")
    sys.stdout.write(value)
    first = False