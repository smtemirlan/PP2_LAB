def countdown(n):
    while n >= 0:
        yield n
        n -= 1

n = int(input("n: "))
for num in countdown(n):
    print(num)