n=int(input())
m=list(map(int,input().split()))
s=set()
for i in m:
    if i in s:
        print("NO")
    else:
        print("YES")
        s.add(i)