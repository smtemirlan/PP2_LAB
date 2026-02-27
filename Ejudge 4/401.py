n=int(input())
def s(n):
    for i in range(1,n+1):
        yield i*i
for x in s(n):
    print(x)