# Copying, backing up, and deleting files

import os
import shutil

source_file = "original.txt"
copy_file = "copy_original.txt"
backup_file = "backup_original.txt"

# Create the source file
with open(source_file, "w", encoding="utf-8") as file:
    file.write("This is the original file\n")

# Copy the file
shutil.copy(source_file, copy_file)
print(f"File copied: {copy_file}")

# Create a backup copy
shutil.copy(source_file, backup_file)
print(f"Backup created: {backup_file}")

# Check if files exist
for file_name in [source_file, copy_file, backup_file]:
    if os.path.exists(file_name):
        print(f"{file_name} exists")

# Safe file deletion
file_to_delete = copy_file

if os.path.exists(file_to_delete):
    os.remove(file_to_delete)
    print(f"{file_to_delete} was deleted")
else:
    print(f"{file_to_delete} was not found")