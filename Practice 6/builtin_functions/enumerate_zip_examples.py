# Examples of enumerate(), zip(), type checking, and type conversion

names = ["Ali", "Aruzhan", "Dana"]
scores = [85, 90, 78]

print("=== enumerate() ===")
for index, name in enumerate(names, start=1):
    print(index, name)

print("\n=== zip() ===")
for name, score in zip(names, scores):
    print(name, score)

print("\n=== Type checking ===")
value1 = 25
value2 = "Hello"
value3 = [1, 2, 3]

print(isinstance(value1, int))
print(isinstance(value2, str))
print(isinstance(value3, list))

print("\n=== Type conversion ===")
text_number = "50"
converted_number = int(text_number)
print(converted_number, type(converted_number))

decimal_number = 9.8
converted_int = int(decimal_number)
print(converted_int, type(converted_int))

tuple_data = (1, 2, 3)
converted_list = list(tuple_data)
print(converted_list, type(converted_list))