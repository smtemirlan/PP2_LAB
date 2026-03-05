import re
def task9(s):
    return re.sub(r"([a-z])([A-Z])", r"\1 \2", s)

print(task9("HelloWorldPython"))
# Hello World Python
