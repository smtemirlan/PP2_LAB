import re
def task1(s):
    pattern = r"ab*"
    return bool(re.fullmatch(pattern, s))

print(task1("a"))        
print(task1("ab"))       
print(task1("abbb"))    
print(task1("ac"))    