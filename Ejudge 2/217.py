n=int(input())
d={}
for i in range(n):
    numbers=input()
    if numbers in d:
        d[numbers]+=1
    else:
        d[numbers]=1
counter=0
for numbers in d:
    if d[numbers]==3:
        counter+=1
print(counter)