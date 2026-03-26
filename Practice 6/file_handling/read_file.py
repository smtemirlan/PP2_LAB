# Reading a file in different ways

file_path = "sample.txt"

# Create a file with sample data if it does not exist
with open(file_path, "w", encoding="utf-8") as file:
    file.write("First line\n")
    file.write("Second line\n")
    file.write("Third line\n")

print("=== read() ===")
with open(file_path, "r", encoding="utf-8") as file:
    content = file.read()
    print(content)

print("=== readline() ===")
with open(file_path, "r", encoding="utf-8") as file:
    print(file.readline().strip())
    print(file.readline().strip())

print("=== readlines() ===")
with open(file_path, "r", encoding="utf-8") as file:
    lines = file.readlines()
    for line in lines:
        print(line.strip())