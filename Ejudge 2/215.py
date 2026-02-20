n=int(input())
names=[]
for i in range(n):
    names.append(input())
print(len(set(names)))