import re
def task5(s):
    pattern = r"a.*b$"
    return bool(re.fullmatch(pattern, s))

print(task5("ab"))         # True
print(task5("axxxb"))      # True
print(task5("axxxbc"))     # False