import re
def task2(s):
    pattern = r"ab{2,3}"
    return bool(re.fullmatch(pattern, s))

print(task2("abb"))      
print(task2("abbb"))     
print(task2("abbbb"))    