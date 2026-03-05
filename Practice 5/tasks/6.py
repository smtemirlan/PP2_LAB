import re
def task6(s):
    pattern = r"[ ,.]"
    return re.sub(pattern, ":", s)

print(task6("Hello, world. Python regex"))
# Hello::world::Python:regex