import os
import shutil


# Recursively copies everything in source_dir into dest_dir
def copy_files_recursive(source_dir, dest_dir):
    # Make the destination folder if it doesn't exist yet
    if not os.path.exists(dest_dir):
        os.mkdir(dest_dir)

    for name in os.listdir(source_dir):
        from_path = os.path.join(source_dir, name)
        to_path = os.path.join(dest_dir, name)
        if os.path.isfile(from_path):
            # A file: copy it over
            print(f" * {from_path} -> {to_path}")
            shutil.copy(from_path, to_path)
        else:
            # A folder: recurse into it
            copy_files_recursive(from_path, to_path)