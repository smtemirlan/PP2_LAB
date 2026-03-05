import re
def task3(s):
    pattern = r"\b[a-z]+_[a-z]+\b"
    return re.findall(pattern, s)

print(task3("hello_world test_text A_bc one_two_three"))
# ['hello_world', 'test_text', 'one_two']