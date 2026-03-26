import re
def task8(s):
    pattern = r"[A-Z][a-z]*"
    return re.findall(pattern, s)

print(task8("HelloWorldPython"))
# ['Hello', 'World', 'Python']