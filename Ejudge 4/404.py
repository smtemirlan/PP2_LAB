a,b=map(int,input().split())
def squars(a,b):
    for i in range(a,b+1):
        yield i*i
for number in squars(a,b):
    print(number)