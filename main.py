from CONFIG import *
import os
from pathlib import Path

def main():
    directory_path = Path(OBSIDIAN_VAULT_PATH).expanduser().resolve()
    print(f"Resolved path: {directory_path}")
    if not directory_path.exists():
        print("Provided path does not exist - exiting program!")
        exit(1)
    data_dict = {}
    parse_md_files(directory_path, data_dict, base_path=directory_path)
    
    # Debug - Print data_dict contents 
    for key in data_dict:
        print("############################################################")
        print(f"\n---------- FILE: {key} ----------\n")
        print(f"{data_dict[key]}\n")
        print("############################################################")


def parse_md_files(path, data_dict, base_path):
    for item in os.listdir(path):
        if item.startswith("."):
            continue
        item_abs_path = os.path.join(path, item)
        rel_path = os.path.relpath(item_abs_path, start=base_path)
        if os.path.isfile(item_abs_path):
            print(item)
            if item_abs_path.endswith(".md"):
                try:
                    with open(item_abs_path, "r", encoding="utf-8") as f:
                        data_dict[rel_path] = f.read()
                except Exception as e:
                    print(f"Exception: {e}")
                    print(f"Error reading file {rel_path}")
                    continue
        else:
            print(f"{item} is a directory...")
            list_files(item_abs_path, data_dict, base_path)

main()