n=int(input())
m=list(map(int,input().split()))
mx=m[0]
for i in m:
    if i>mx:
        mx=i
print(mx)