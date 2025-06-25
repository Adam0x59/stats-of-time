from CONFIG import *
import os
from functions.doc_parse import *

def main():

    # Identify and parse .md files from directories in OBSIDIAN_VALUT_PATH
    # recursively and store content in data_dict to await further processing
    directory_path = os.path.abspath(os.path.expanduser(OBSIDIAN_VAULT_PATH))
    #print(f"Resolved path: {directory_path}")
    if not os.path.exists(directory_path):
        print("Provided path does not exist - exiting program!")
        exit(1)
    data_dict = {}
    parse_md_files(directory_path, data_dict, base_path=directory_path)
    # Parse items stored in data_dict, extract metadata, tasks and calculate
    # word count. Store data alongside content in data_dict.
    extract_metadata(data_dict)
    extract_tasks(data_dict)
    extract_wordcount(data_dict)


    # Debug - Print data_dict contents to terminal
    '''
    for key in data_dict:
        print("############################################################")
        print(f"\n---------- FILE: {key} ----------\n")
        print(f"\nCONTENT:\n\n{repr(data_dict[key]['content'])}\n")
        if "metadata" in data_dict[key]:
            print(f"\nMETADATA:\n\n{repr(data_dict[key]['metadata'])}\n")
        #print(f"{data_dict[key]}")
        print("############################################################")
    '''
    for key in data_dict:
        print("############################################################")
        for sub_key in data_dict[key]:
            print(f"\n{sub_key}:\n----\n{data_dict[key][sub_key]}\n----\n")
        print("############################################################\n")
main()