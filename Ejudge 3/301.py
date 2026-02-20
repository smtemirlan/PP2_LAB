n=input()
valid=True
for i in n:
    if int(i)%2!=0:
        valid=False
        break
if valid:
    print("Valid")
else:
    print("Not valid")