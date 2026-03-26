# Examples of map(), filter(), reduce(), len(), sum(), min(), max(), sorted()

from functools import reduce

numbers = [1, 2, 3, 4, 5, 6]

# map() - multiply each element by 2
mapped = list(map(lambda x: x * 2, numbers))
print("map():", mapped)

# filter() - keep only even numbers
filtered = list(filter(lambda x: x % 2 == 0, numbers))
print("filter():", filtered)

# reduce() - sum of all elements
reduced = reduce(lambda x, y: x + y, numbers)
print("reduce():", reduced)

# Other built-in functions
print("len():", len(numbers))
print("sum():", sum(numbers))
print("min():", min(numbers))
print("max():", max(numbers))

# sorted()
unsorted_numbers = [5, 2, 8, 1, 3]
print("sorted():", sorted(unsorted_numbers))

# Type conversion
num_str = "100"
num_int = int(num_str)
print("int():", num_int)

float_str = "12.5"
num_float = float(float_str)
print("float():", num_float)

print("str():", str(500))
print("list():", list("Python"))