x=int(input())
is_prime=True
for i in range(2,x):
    if x%i==0:
        is_prime=False
        break
if(is_prime):
    print("Yes")
else:
    print("No")