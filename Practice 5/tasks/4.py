import re
def task4(s):
    pattern = r"\b[A-Z][a-z]+\b"
    return re.findall(pattern, s)

print(task4("Hello world My name is Arman"))
# ['Hello', 'My', 'Arman']