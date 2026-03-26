# Creating directories, listing contents, and getting current directory

import os
from pathlib import Path

base_dir = "practice_dirs"
nested_dir = os.path.join(base_dir, "folder1", "folder2")

# Create nested directories
os.makedirs(nested_dir, exist_ok=True)
print(f"Created path: {nested_dir}")

# Current working directory
print("Current directory:", os.getcwd())

# List files and folders
print("\nContents of the current directory:")
for item in os.listdir():
    print(item)

# Create a directory using pathlib
path_obj = Path("practice_dirs/folder3")
path_obj.mkdir(parents=True, exist_ok=True)
print(f"\nDirectory created with pathlib: {path_obj}")

# Change directory
os.chdir(base_dir)
print("\nAfter os.chdir():", os.getcwd())

print("\nContents of practice_dirs:")
for item in os.listdir():
    print(item)