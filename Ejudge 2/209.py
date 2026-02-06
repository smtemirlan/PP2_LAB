n=int(input())
m=list(map(int,input().split()))
mx=m[0]
for i in range(n):
    if m[i]>mx:
        mx=m[i]
mn=m[0]
for i in range(n):
    if m[i]<mn:
        mn=m[i]
for i in range(n):
    if m[i]==mx:
        m[i]=mn
print(*m)