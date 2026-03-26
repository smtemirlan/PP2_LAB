import sys

n = int(input())

def prime_generator(limit):
    if limit >= 2:
        yield 2
    for num in range(3, limit + 1, 2):
        is_prime = True
        for i in range(3, int(num ** 0.5) + 1, 2):
            if num % i == 0:
                is_prime = False
                break
        if is_prime:
            yield num

first = True
for p in prime_generator(n):
    if not first:
        sys.stdout.write(" ")
    sys.stdout.write(str(p))
    first = False