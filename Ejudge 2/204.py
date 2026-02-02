n=int(input())
m=input().split()
counter=0
for i in m:
    if int(i)>0:
        counter+=1
print(counter)