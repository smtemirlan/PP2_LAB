n=int(input())
m=list(map(int,input().split()))
mx=m[0]
index=1
for i in range(n):
    if m[i]>mx:
        mx=m[i]
        index=i+1
print(index)