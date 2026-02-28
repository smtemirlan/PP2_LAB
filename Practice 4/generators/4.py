def squares(a, b):
    for i in range(a, b + 1):
        yield i * i


a = int(input("a: "))
b = int(input("b: "))

for value in squares(a, b):
    print(value)