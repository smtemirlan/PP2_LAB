n=int(input())
m=list(map(int,input().split()))
a=[x**2 for x in m]
print(*a)