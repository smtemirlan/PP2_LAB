# Finding files by extension, moving and copying files

import os
import shutil

source_dir = "source_files"
target_dir = "target_files"

os.makedirs(source_dir, exist_ok=True)
os.makedirs(target_dir, exist_ok=True)

# Create test files
with open(os.path.join(source_dir, "file1.txt"), "w", encoding="utf-8") as f:
    f.write("Text file 1")

with open(os.path.join(source_dir, "file2.txt"), "w", encoding="utf-8") as f:
    f.write("Text file 2")

with open(os.path.join(source_dir, "image.jpg"), "w", encoding="utf-8") as f:
    f.write("This is not a real image, just an example")

# Find files with .txt extension
print("Files with .txt extension:")
for file_name in os.listdir(source_dir):
    if file_name.endswith(".txt"):
        print(file_name)

# Copy a file
shutil.copy(
    os.path.join(source_dir, "file1.txt"),
    os.path.join(target_dir, "file1_copy.txt")
)
print("\nfile1.txt was copied to target_files")

# Move a file
shutil.move(
    os.path.join(source_dir, "file2.txt"),
    os.path.join(target_dir, "file2_moved.txt")
)
print("file2.txt was moved to target_files")