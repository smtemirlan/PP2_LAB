txt=input()
digit=0
letter=0
space=0
for ch in txt:
    if ch.isdigit():
        digit+=1
    elif ch.isalpha():
        letter+=1
    elif ch.isspace():
        space+=1
print(digit)
print(letter)
print(space)    